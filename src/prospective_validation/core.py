from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


LEGS = (
    ("P35_PE", "PE", 1, 0.35),
    ("P20_PE", "PE", -2, 0.20),
    ("P65_CE", "CE", 1, 0.65),
    ("P80_CE", "CE", -2, 0.80),
)


@dataclass(frozen=True)
class LegQuote:
    bid: float | None
    ask: float | None
    ltp: float | None


def normalize_chain(rows: list[dict[str, Any]]) -> pd.DataFrame:
    out = pd.DataFrame(rows)
    if out.empty:
        raise ValueError("empty option chain")
    aliases = {
        "strikePrice":"strike",
        "lastPrice":"ltp",
        "optionType":"option_type",
        "optType":"option_type",
        "expiryDate":"expiry",
        "bidPrice":"bid",
        "offerPrice":"ask",
    }
    for src, dst in aliases.items():
        if src in out.columns and dst not in out.columns:
            out[dst] = out[src]
    required = {"strike","option_type","ltp"}
    missing = required - set(out.columns)
    if missing:
        raise ValueError(f"chain missing columns: {sorted(missing)}")
    for c in ("strike","ltp","bid","ask"):
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
    out["option_type"] = out["option_type"].astype(str).str.upper().replace({"CALL":"CE","PUT":"PE"})
    if "expiry" in out.columns:
        out["expiry"] = pd.to_datetime(out["expiry"], errors="coerce").dt.normalize()
    return out


def historical_log_returns(close_series: pd.Series, signal_date: pd.Timestamp, window: int = 756) -> np.ndarray:
    x = pd.DataFrame({"date": pd.to_datetime(close_series.index), "close": pd.to_numeric(close_series.values, errors="coerce")})
    x = x.sort_values("date")
    x = x[x["date"] < pd.Timestamp(signal_date).normalize()]
    x["logret"] = np.log(x["close"]).diff()
    out = x["logret"].dropna().to_numpy(dtype=float)
    out = out[np.isfinite(out)]
    if out.size < window:
        raise ValueError(f"need {window} finite historical returns; got {out.size}")
    return out[-window:]


def simulate_terminal_paths(s0: float, returns: np.ndarray, horizon: int = 3, paths: int = 5000, seed: int = 756) -> np.ndarray:
    if s0 <= 0:
        raise ValueError("s0 must be positive")
    r = np.asarray(returns, dtype=float)
    r = r[np.isfinite(r)]
    if r.size < 756:
        raise ValueError("MC-RQ6-v1 requires 756 finite returns")
    r = r[-756:]
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, r.size, size=(paths, horizon))
    return s0 * np.exp(r[idx].sum(axis=1))


def quantile_targets(terminals: np.ndarray) -> dict[str,float]:
    return {
        "P20_PE": float(np.quantile(terminals, 0.20)),
        "P35_PE": float(np.quantile(terminals, 0.35)),
        "P65_CE": float(np.quantile(terminals, 0.65)),
        "P80_CE": float(np.quantile(terminals, 0.80)),
    }


def choose_unique_strikes(chain: pd.DataFrame, targets: dict[str,float]) -> dict[str,float]:
    chosen: dict[str,float] = {}
    used: set[float] = set()
    for label in ("P20_PE","P35_PE","P65_CE","P80_CE"):
        side = "PE" if label.endswith("PE") else "CE"
        strikes = sorted(float(x) for x in chain.loc[chain["option_type"]==side,"strike"].dropna().unique())
        if not strikes:
            raise ValueError(f"no strikes for {side}")
        ordered = sorted(strikes, key=lambda k: (abs(k-targets[label]), k))
        for k in ordered:
            if k not in used:
                chosen[label] = k
                used.add(k)
                break
        if label not in chosen:
            raise ValueError(f"unable to choose unique strike for {label}")
    return chosen


def parity_spot(chain: pd.DataFrame, previous_close: float) -> tuple[float,str]:
    ce = chain.loc[chain["option_type"]=="CE",["strike","ltp"]].rename(columns={"ltp":"ce"})
    pe = chain.loc[chain["option_type"]=="PE",["strike","ltp"]].rename(columns={"ltp":"pe"})
    m = ce.merge(pe, on="strike", how="inner")
    if m.empty:
        return float(previous_close), "previous_close_fallback"
    m["spot_hat"] = m["strike"] + m["ce"] - m["pe"]
    m = m.replace([np.inf,-np.inf],np.nan).dropna(subset=["spot_hat"])
    m = m[m["spot_hat"]>0]
    if m.empty:
        return float(previous_close), "previous_close_fallback"
    band = m[np.abs(m["strike"]-previous_close) <= 0.02*previous_close]
    if band.empty:
        return float(previous_close), "previous_close_fallback"
    return float(band["spot_hat"].median()), "put_call_parity_snapshot"


def portfolio_mc_ev(terminals: np.ndarray, strikes: dict[str,float], chain: pd.DataFrame) -> float:
    payoff = np.zeros_like(terminals, dtype=float)
    entry = 0.0
    for label, side, qty, _ in LEGS:
        k = strikes[label]
        intrinsic = np.maximum(k-terminals,0.0) if side=="PE" else np.maximum(terminals-k,0.0)
        payoff += qty * intrinsic
        p = chain.loc[(chain["option_type"]==side) & (chain["strike"]==k),"ltp"]
        if p.empty:
            raise ValueError(f"missing gate price {label}")
        entry += qty * float(p.iloc[-1])
    return float(np.mean(payoff) - entry)


def best_quote(chain: pd.DataFrame, side: str, strike: float) -> LegQuote:
    x = chain.loc[(chain["option_type"]==side) & (chain["strike"]==float(strike))]
    if x.empty:
        raise ValueError(f"missing quote {side} {strike}")
    r = x.iloc[-1]
    return LegQuote(
        bid=None if pd.isna(r.get("bid")) else float(r["bid"]),
        ask=None if pd.isna(r.get("ask")) else float(r["ask"]),
        ltp=None if pd.isna(r.get("ltp")) else float(r["ltp"]),
    )


def entry_price(quote: LegQuote, qty: int, slippage_points: float = 2.0) -> tuple[float,str]:
    if qty > 0 and quote.ask and quote.ask > 0:
        return quote.ask + slippage_points, "ask_plus_slippage"
    if qty < 0 and quote.bid and quote.bid > 0:
        return quote.bid - slippage_points, "bid_minus_slippage"
    if quote.ltp and quote.ltp > 0:
        return quote.ltp + slippage_points if qty>0 else max(quote.ltp-slippage_points,0.0), "ltp_plus_or_minus_slippage"
    raise ValueError("no executable price")


def mark_price(quote: LegQuote, qty: int) -> tuple[float,str]:
    if qty > 0 and quote.bid and quote.bid > 0:
        return quote.bid, "bid"
    if qty < 0 and quote.ask and quote.ask > 0:
        return quote.ask, "ask"
    if quote.ltp and quote.ltp > 0:
        return quote.ltp, "ltp_fallback"
    raise ValueError("no mark price")


def mark_pnl_rupees(position: dict[str,Any], chain: pd.DataFrame) -> tuple[float,dict[str,Any]]:
    point_pnl = 0.0
    marks={}
    strikes=position["strikes"]
    entry=position["entry_prices"]
    for label, side, qty, _ in LEGS:
        q=best_quote(chain,side,float(strikes[label]))
        px, source=mark_price(q,qty)
        point_pnl += qty*(px-float(entry[label]))
        marks[label]={"price":px,"source":source,"bid":q.bid,"ask":q.ask,"ltp":q.ltp}
    return float(point_pnl*position["lot_size"]), marks


def expiry_pnl_rupees(position: dict[str,Any], settlement_spot: float) -> float:
    point_pnl=0.0
    for label, side, qty, _ in LEGS:
        k=float(position["strikes"][label])
        intrinsic=max(k-settlement_spot,0.0) if side=="PE" else max(settlement_spot-k,0.0)
        point_pnl += qty*(intrinsic-float(position["entry_prices"][label]))
    return float(point_pnl*position["lot_size"])


def d3_sessions(expiry: pd.Timestamp, holidays: set[date]) -> list[date]:
    out=[]
    cur=pd.Timestamp(expiry).date()-timedelta(days=1)
    while len(out)<3:
        if cur.weekday()<5 and cur not in holidays:
            out.append(cur)
        cur -= timedelta(days=1)
    return list(reversed(out))


def is_d3(today: date, expiry: date, holidays: set[date]) -> bool:
    return today == d3_sessions(pd.Timestamp(expiry),holidays)[0]


def stable_id(payload: dict[str,Any]) -> str:
    raw=json.dumps(payload,sort_keys=True,default=str,separators=(",",":")).encode()
    return hashlib.sha256(raw).hexdigest()[:20]
