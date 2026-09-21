from __future__ import annotations

import os
from datetime import datetime, date, time, timedelta
from typing import Any

import pandas as pd

from .calendar import holidays
from .core import (
    historical_log_returns, simulate_terminal_paths, quantile_targets,
    choose_unique_strikes, parity_spot, portfolio_mc_ev, best_quote,
    entry_price, mark_pnl_rupees, expiry_pnl_rupees, is_d3, stable_id,
)
from .market import live_chain, fetch_yahoo_daily
from .store import append_jsonl, open_positions, write_snapshot, now_utc

from src.model.costs import enhanced_entry_costs, expiry_stt


IST = "Asia/Kolkata"
SLIPPAGE = 2.0
INDEX_TICKERS = {"NIFTY": "^NSEI", "SENSEX": "^BSESN"}
SIGNAL_START = time(9, 25)
SIGNAL_END = time(9, 40)


def _now_ist() -> pd.Timestamp:
    return pd.Timestamp.now(tz=IST)


def _today_ist() -> date:
    return _now_ist().date()


def _run_record(run_id: str, mode: str, status: str, extra: dict[str, Any] | None = None) -> None:
    rec = {
        "timestamp_utc": now_utc(),
        "run_id": run_id,
        "mode": mode,
        "status": status,
        "repository_revision": os.environ.get("GITHUB_SHA"),
    }
    if extra:
        rec.update(extra)
    append_jsonl("runs.jsonl", rec)


def _lot_size(underlying: str, expiry: date, chain: pd.DataFrame) -> tuple[int, str]:
    if "lot_size" in chain.columns:
        vals = pd.to_numeric(chain["lot_size"], errors="coerce").dropna().astype(int).unique()
        if len(vals) == 1 and vals[0] > 0:
            return int(vals[0]), "provider_contract_metadata"
    if underlying == "NIFTY" and expiry >= date(2026, 1, 6):
        return 65, "locked_2026_schedule_fallback"
    if underlying == "SENSEX" and expiry >= date(2024, 11, 20):
        return 20, "locked_2026_schedule_fallback"
    raise RuntimeError(f"no authoritative lot-size rule for {underlying} {expiry}")


def _signal_timing(now: pd.Timestamp) -> tuple[bool, str]:
    t = now.timetz().replace(tzinfo=None)
    if SIGNAL_START <= t <= SIGNAL_END:
        return True, "09:30_window"
    return False, "outside_09:30_window"


def _existing_signal(signal_id: str) -> bool:
    from .store import read_jsonl
    return any(s.get("signal_id") == signal_id and s.get("prospective_valid") for s in read_jsonl("signals.jsonl"))


def scan(underlying_filter: str = "BOTH", force_today: bool = False) -> None:
    run_id = stable_id({"mode": "scan", "now": now_utc(), "underlying": underlying_filter})
    _run_record(run_id, "scan", "STARTED")
    underlyings = ["NIFTY", "SENSEX"] if underlying_filter == "BOTH" else [underlying_filter]

    for underlying in underlyings:
        observed = _now_ist()
        try:
            chain, meta = live_chain(underlying)
            chain = chain.copy()
            if "expiry" not in chain.columns:
                raise ValueError("live chain has no expiry field")
            chain["expiry"] = pd.to_datetime(chain["expiry"], errors="coerce").dt.normalize()
            today = observed.date()
            expiries = sorted(x.date() for x in chain["expiry"].dropna().unique() if x.date() >= today)
            if not expiries:
                raise RuntimeError("no future expiry in live chain")
            expiry = expiries[0]

            h = holidays(underlying, expiry.year)
            d3 = is_d3(today, expiry, h)
            timing_ok, timing_status = _signal_timing(observed)
            prospective_valid = bool(d3 and timing_ok and not force_today)
            manual_forced = bool(force_today and not d3)

            base = {
                "underlying": underlying,
                "expiry": str(expiry),
                "scan_date": str(today),
                "observed_timestamp_ist": observed.isoformat(),
                "d3_expected": d3,
                "timing_status": timing_status,
                "prospective_valid": prospective_valid,
                "manual_forced": manual_forced,
                "data_source": meta.get("source"),
            }

            if not d3 and not force_today:
                append_jsonl("signals.jsonl", {
                    **base,
                    "signal_id": stable_id(base),
                    "trade": False,
                    "gate": False,
                    "status": "NOT_D3",
                    "reason": "today_is_not_D3",
                })
                continue

            if force_today and not d3:
                append_jsonl("signals.jsonl", {
                    **base,
                    "signal_id": stable_id(base),
                    "trade": False,
                    "gate": False,
                    "status": "MANUAL_DIAGNOSTIC",
                    "reason": "force_today_is_diagnostic_only",
                })
                continue

            if not timing_ok:
                append_jsonl("signals.jsonl", {
                    **base,
                    "signal_id": stable_id(base),
                    "trade": False,
                    "gate": False,
                    "status": "TIMING_INVALID",
                    "reason": "outside_09:30_window",
                })
                continue

            signal_id = stable_id({"underlying": underlying, "expiry": str(expiry), "d3": str(today)})
            if _existing_signal(signal_id):
                append_jsonl("signals.jsonl", {
                    **base,
                    "signal_id": signal_id,
                    "trade": False,
                    "gate": False,
                    "status": "D3_ALREADY_CAPTURED",
                    "reason": "prospective_signal_already_logged",
                })
                continue

            target_chain = chain.loc[chain["expiry"] == pd.Timestamp(expiry)].copy()
            if target_chain.empty:
                raise RuntimeError(f"live chain has no rows for target expiry {expiry}")

            daily = fetch_yahoo_daily(INDEX_TICKERS[underlying], years=5)
            prior = daily[daily.index < pd.Timestamp(today)]
            if prior.empty:
                raise RuntimeError("missing previous close")
            previous_close = float(prior.iloc[-1])
            returns = historical_log_returns(daily, pd.Timestamp(today), 756)
            s0, s0_source = parity_spot(target_chain, previous_close)

            terminals = simulate_terminal_paths(s0, returns, horizon=3, paths=5000, seed=756)
            targets = quantile_targets(terminals)
            strikes = choose_unique_strikes(target_chain, targets)
            ev = portfolio_mc_ev(terminals, strikes, target_chain)

            sig = {
                **base,
                "signal_id": signal_id,
                "status": "EVALUATED",
                "mc_ev_points": ev,
                "gate": ev > 0,
                "trade": False,
                "s0": s0,
                "s0_source": s0_source,
                "quantile_targets": targets,
                "strikes": strikes,
                "terminal_mean": float(terminals.mean()),
                "terminal_p05": float(pd.Series(terminals).quantile(.05)),
                "terminal_p95": float(pd.Series(terminals).quantile(.95)),
                "strategy_version": "BATMAN-MC-RQ6-v1-PAPER",
            }

            write_snapshot(
                f"{underlying}_{expiry}_{today}_signal",
                {
                    "run_id": run_id,
                    "underlying": underlying,
                    "expiry": str(expiry),
                    "signal_date": str(today),
                    "observed_timestamp_ist": observed.isoformat(),
                    "provider_meta": meta,
                    "chain": chain.to_dict(orient="records"),
                    "mc": {
                        "s0": s0,
                        "s0_source": s0_source,
                        "returns_count": len(returns),
                        "paths": 5000,
                        "seed": 756,
                        "horizon": 3,
                    },
                    "targets": targets,
                    "strikes": strikes,
                    "mc_ev_points": ev,
                },
            )

            positions = open_positions()
            already = any(p.get("signal_id") == signal_id for p in positions.values())
            if ev > 0 and not already:
                entry = {}
                entry_sources = {}
                quantities = {"P35_PE": 1, "P20_PE": -2, "P65_CE": 1, "P80_CE": -2}

                for label, side, qty in [
                    ("P35_PE", "PE", 1), ("P20_PE", "PE", -2),
                    ("P65_CE", "CE", 1), ("P80_CE", "CE", -2)
                ]:
                    ep, src = entry_price(best_quote(target_chain, side, strikes[label]), qty, SLIPPAGE)
                    entry[label] = ep
                    entry_sources[label] = src

                lot, lot_source = _lot_size(underlying, expiry, target_chain)
                cost_model = enhanced_entry_costs(
                    underlying=underlying,
                    prices=entry,
                    quantities=quantities,
                    lot_size=lot,
                    trade_date=pd.Timestamp(today),
                )

                pid = stable_id({"signal_id": signal_id, "entry": entry})
                position = {
                    "position_id": pid,
                    "signal_id": signal_id,
                    "underlying": underlying,
                    "expiry": str(expiry),
                    "signal_date": str(today),
                    "opened_at_utc": now_utc(),
                    "lot_size": lot,
                    "lot_size_source": lot_source,
                    "strikes": strikes,
                    "entry_prices": entry,
                    "entry_price_sources": entry_sources,
                    "entry_costs_estimate": cost_model,
                    "slippage_points_per_leg": SLIPPAGE,
                    "paper_only": True,
                }
                append_jsonl("events.jsonl", {
                    "event_type": "OPEN",
                    "timestamp_utc": now_utc(),
                    "position_id": pid,
                    "position": position,
                })
                sig.update({
                    "trade": True,
                    "paper_position_id": pid,
                    "paper_entry": entry,
                    "lot_size": lot,
                    "lot_size_source": lot_source,
                    "estimated_entry_cost_rupees": cost_model["total_enhanced_entry_cost"],
                })

            append_jsonl("signals.jsonl", sig)

        except Exception as exc:
            rec = {
                "timestamp_utc": now_utc(),
                "run_id": run_id,
                "underlying": underlying,
                "mode": "scan",
                "error_type": type(exc).__name__,
                "message": str(exc),
            }
            append_jsonl("errors.jsonl", rec)
            append_jsonl("signals.jsonl", {
                "signal_id": stable_id(rec),
                "underlying": underlying,
                "scan_date": str(_today_ist()),
                "observed_timestamp_ist": observed.isoformat(),
                "prospective_valid": False,
                "status": "ERROR",
                "trade": False,
                "gate": False,
                "reason": "DATA_UNAVAILABLE_OR_ERROR",
                "error": str(exc),
            })
    _run_record(run_id, "scan", "DONE")


def _close_if_expired(pid: str, pos: dict[str, Any], observed: pd.Timestamp) -> None:
    expiry = date.fromisoformat(pos["expiry"])
    if observed.date() < expiry or observed.time() < time(15, 35):
        return
    daily = fetch_yahoo_daily(INDEX_TICKERS[pos["underlying"]], years=2)
    rows = daily[daily.index <= pd.Timestamp(expiry)]
    if rows.empty:
        raise RuntimeError("missing expiry settlement close")
    settlement = float(rows.iloc[-1])
    strikes = pos["strikes"]
    quantities = {"P35_PE": 1, "P20_PE": -2, "P65_CE": 1, "P80_CE": -2}
    expiry_cost = expiry_stt(pd.Timestamp(expiry), settlement, strikes, quantities, int(pos["lot_size"]))
    gross = expiry_pnl_rupees(pos, settlement)
    entry_cost = float(pos.get("entry_costs_estimate", {}).get("total_enhanced_entry_cost", 0.0))
    net = gross - entry_cost - expiry_cost
    append_jsonl("events.jsonl", {
        "event_type": "CLOSE",
        "timestamp_utc": now_utc(),
        "position_id": pid,
        "reason": "expiry_settlement",
        "settlement_spot": settlement,
        "gross_realized_pnl_rupees": gross,
        "entry_cost_rupees": entry_cost,
        "expiry_stt_rupees": expiry_cost,
        "realized_pnl_rupees_net": net,
    })


def mark(underlying_filter: str = "BOTH") -> None:
    run_id = stable_id({"mode": "mark", "now": now_utc(), "underlying": underlying_filter})
    _run_record(run_id, "mark", "STARTED")
    positions = open_positions()
    for pid, pos in positions.items():
        if underlying_filter != "BOTH" and pos["underlying"] != underlying_filter:
            continue
        observed = _now_ist()
        try:
            expiry = date.fromisoformat(pos["expiry"])
            if observed.date() > expiry or (observed.date() == expiry and observed.time() >= time(15, 35)):
                _close_if_expired(pid, pos, observed)
                continue

            chain, meta = live_chain(pos["underlying"])
            chain = chain.copy()
            if "expiry" in chain.columns:
                chain["expiry"] = pd.to_datetime(chain["expiry"], errors="coerce").dt.normalize()
            expiry_chain = chain.loc[chain["expiry"] == pd.Timestamp(expiry)].copy()
            if expiry_chain.empty:
                raise RuntimeError(f"live chain has no rows for open position expiry {expiry}")
            pnl, marks = mark_pnl_rupees(pos, expiry_chain)
            entry_cost = float(pos.get("entry_costs_estimate", {}).get("total_enhanced_entry_cost", 0.0))
            append_jsonl("events.jsonl", {
                "event_type": "MARK",
                "timestamp_utc": now_utc(),
                "position_id": pid,
                "underlying": pos["underlying"],
                "expiry": pos["expiry"],
                "pnl_rupees": pnl,
                "pnl_rupees_net_estimate": pnl - entry_cost,
                "entry_cost_rupees": entry_cost,
                "marks": marks,
                "data_source": meta.get("source"),
                "observed_timestamp_ist": observed.isoformat(),
            })
        except Exception as exc:
            append_jsonl("errors.jsonl", {
                "timestamp_utc": now_utc(),
                "run_id": run_id,
                "position_id": pid,
                "mode": "mark",
                "error_type": type(exc).__name__,
                "message": str(exc),
            })
    _run_record(run_id, "mark", "DONE")


def _today_ist() -> date:
    return _now_ist().date()
