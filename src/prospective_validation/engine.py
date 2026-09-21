from __future__ import annotations

import json
import os
from datetime import datetime, date
from pathlib import Path
from typing import Any

import pandas as pd

from .calendar import holidays
from .core import (
    historical_log_returns, simulate_terminal_paths, quantile_targets,
    choose_unique_strikes, parity_spot, portfolio_mc_ev, best_quote,
    entry_price, mark_pnl_rupees, expiry_pnl_rupees, is_d3, stable_id,
)
from .market import live_chain, fetch_yahoo_daily
from .store import append_jsonl, open_positions, read_jsonl, write_snapshot, now_utc


IST="Asia/Kolkata"
ROOT=Path(__file__).resolve().parents[2]
SLIPPAGE=2.0
INDEX_TICKERS={"NIFTY":"^NSEI","SENSEX":"^BSESN"}


def _today_ist() -> date:
    return pd.Timestamp.now(tz=IST).date()


def _run_record(run_id: str, mode: str, status: str, extra: dict[str,Any]|None=None) -> None:
    rec={"timestamp_utc":now_utc(),"run_id":run_id,"mode":mode,"status":status,"repository_revision":os.environ.get("GITHUB_SHA")}
    if extra: rec.update(extra)
    append_jsonl("runs.jsonl",rec)


def scan(underlying_filter: str="BOTH", force_today: bool=False) -> None:
    run_id=stable_id({"mode":"scan","now":now_utc()})
    _run_record(run_id,"scan","STARTED")
    underlyings=["NIFTY","SENSEX"] if underlying_filter=="BOTH" else [underlying_filter]
    for underlying in underlyings:
        try:
            chain,meta=live_chain(underlying)
            chain=chain.copy()
            chain["expiry"]=pd.to_datetime(chain["expiry"],errors="coerce").dt.normalize() if "expiry" in chain.columns else pd.NaT
            expiries=sorted(x.date() for x in chain["expiry"].dropna().unique() if x.date() >= _today_ist())
            if not expiries:
                raise RuntimeError("no future expiry in live chain")
            expiry=expiries[0]
            h=holidays(underlying,expiry.year)
            d3=is_d3(_today_ist(),expiry,h)
            base={"underlying":underlying,"expiry":str(expiry),"scan_date":str(_today_ist()),"d3_expected":d3,"data_source":meta.get("source")}
            if not d3 and not force_today:
                append_jsonl("signals.jsonl",{**base,"signal_id":stable_id(base),"trade":False,"gate":False,"status":"NOT_D3","reason":"today_is_not_D3"})
                continue

            ticker=INDEX_TICKERS[underlying]
            daily=fetch_yahoo_daily(ticker,years=5)
            prev=float(daily[daily.index < pd.Timestamp(_today_ist())].iloc[-1])
            returns=historical_log_returns(daily,pd.Timestamp(_today_ist()),756)
            s0,s0_source=parity_spot(chain,prev)
            terminals=simulate_terminal_paths(s0,returns,horizon=3,paths=5000,seed=756)
            targets=quantile_targets(terminals)
            strikes=choose_unique_strikes(chain,targets)
            ev=portfolio_mc_ev(terminals,strikes,chain)
            sid=stable_id({"underlying":underlying,"expiry":str(expiry),"d3":str(_today_ist())})
            sig={
                **base,"signal_id":sid,"status":"EVALUATED","mc_ev_points":ev,
                "gate":ev>0,"trade":False,"s0":s0,"s0_source":s0_source,
                "quantile_targets":targets,"strikes":strikes,
                "terminal_mean":float(terminals.mean()),"terminal_p05":float(pd.Series(terminals).quantile(.05)),
                "terminal_p95":float(pd.Series(terminals).quantile(.95)),
                "strategy_version":"BATMAN-MC-RQ6-v1-PAPER"
            }
            # Snapshot the exact source inputs used by the signal.
            write_snapshot(f"{underlying}_{expiry}_{_today_ist()}_signal",{
                "run_id":run_id,"underlying":underlying,"expiry":str(expiry),"signal_date":str(_today_ist()),
                "provider_meta":meta,"chain":chain.to_dict(orient="records"),
                "mc":{"s0":s0,"s0_source":s0_source,"returns_count":len(returns),"paths":5000,"seed":756,"horizon":3},
                "targets":targets,"strikes":strikes,"mc_ev_points":ev
            })

            positions=open_positions()
            already=any(p.get("signal_id")==sid for p in positions.values())
            if ev>0 and not already:
                entry={}
                entry_sources={}
                for label,side,qty,_ in [
                    ("P35_PE","PE",1,.35),("P20_PE","PE",-2,.20),
                    ("P65_CE","CE",1,.65),("P80_CE","CE",-2,.80)
                ]:
                    ep,src=entry_price(best_quote(chain,side,strikes[label]),qty,SLIPPAGE)
                    entry[label]=ep; entry_sources[label]=src
                lot=65 if underlying=="NIFTY" else 20
                pid=stable_id({"signal_id":sid,"entry":entry})
                position={
                    "position_id":pid,"signal_id":sid,"underlying":underlying,"expiry":str(expiry),
                    "signal_date":str(_today_ist()),"opened_at_utc":now_utc(),
                    "lot_size":lot,"strikes":strikes,"entry_prices":entry,"entry_price_sources":entry_sources,
                    "slippage_points_per_leg":SLIPPAGE,"paper_only":True
                }
                append_jsonl("events.jsonl",{"event_type":"OPEN","timestamp_utc":now_utc(),"position_id":pid,"position":position})
                sig.update({"trade":True,"paper_position_id":pid,"paper_entry":entry})
            append_jsonl("signals.jsonl",sig)
        except Exception as exc:
            rec={"timestamp_utc":now_utc(),"run_id":run_id,"underlying":underlying,"mode":"scan","error_type":type(exc).__name__,"message":str(exc)}
            append_jsonl("errors.jsonl",rec)
            append_jsonl("signals.jsonl",{"signal_id":stable_id(rec),"underlying":underlying,"scan_date":str(_today_ist()),"status":"ERROR","trade":False,"gate":False,"reason":"DATA_UNAVAILABLE_OR_ERROR","error":str(exc)})
    _run_record(run_id,"scan","DONE")


def mark(underlying_filter: str="BOTH") -> None:
    run_id=stable_id({"mode":"mark","now":now_utc()})
    _run_record(run_id,"mark","STARTED")
    positions=open_positions()
    for pid,pos in positions.items():
        if underlying_filter!="BOTH" and pos["underlying"]!=underlying_filter:
            continue
        try:
            chain,meta=live_chain(pos["underlying"])
            chain=chain.copy()
            chain["expiry"]=pd.to_datetime(chain["expiry"],errors="coerce").dt.normalize()
            pnl,marks=mark_pnl_rupees(pos,chain)
            append_jsonl("events.jsonl",{
                "event_type":"MARK","timestamp_utc":now_utc(),"position_id":pid,
                "underlying":pos["underlying"],"expiry":pos["expiry"],"pnl_rupees":pnl,
                "marks":marks,"data_source":meta.get("source")
            })
            expiry=date.fromisoformat(pos["expiry"])
            if _today_ist()>expiry:
                daily=fetch_yahoo_daily(INDEX_TICKERS[pos["underlying"]],years=2)
                settlement=float(daily[daily.index<=pd.Timestamp(expiry)].iloc[-1])
                realized=expiry_pnl_rupees(pos,settlement)
                append_jsonl("events.jsonl",{
                    "event_type":"CLOSE","timestamp_utc":now_utc(),"position_id":pid,
                    "reason":"expiry_settlement","settlement_spot":settlement,
                    "realized_pnl_rupees":realized
                })
        except Exception as exc:
            append_jsonl("errors.jsonl",{"timestamp_utc":now_utc(),"run_id":run_id,"position_id":pid,"mode":"mark","error_type":type(exc).__name__,"message":str(exc)})
    _run_record(run_id,"mark","DONE")
