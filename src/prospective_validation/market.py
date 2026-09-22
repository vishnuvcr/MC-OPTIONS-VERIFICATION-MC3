from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd
import requests


IST = "Asia/Kolkata"
ROOT = Path(__file__).resolve().parents[2]
CACHE_ROOT = ROOT / "data" / "paper" / "market_cache"
NSE_URL = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
NSE_HOME = "https://www.nseindia.com"


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
        "Accept": "application/json,text/plain,*/*",
        "Accept-Language": "en-US,en;q=0.8",
        "Referer": NSE_HOME + "/option-chain",
        "Connection": "keep-alive",
    })
    return s


def _cache_paths(ticker: str) -> tuple[Path, Path]:
    safe = ticker.replace("/", "_").replace("^", "")
    return CACHE_ROOT / f"{safe}_daily.csv", CACHE_ROOT / f"{safe}_daily.meta.json"


def _read_daily_cache(ticker: str) -> pd.Series | None:
    csv_path, _ = _cache_paths(ticker)
    if not csv_path.exists():
        return None
    try:
        df = pd.read_csv(csv_path)
        dates = pd.to_datetime(df["date"], errors="coerce")
        closes = pd.to_numeric(df["close"], errors="coerce")
        out = pd.Series(closes.to_numpy(dtype=float), index=dates, name="close").dropna()
        out = out[~out.index.duplicated(keep="last")].sort_index()
        return out if not out.empty else None
    except Exception:
        return None


def _write_daily_cache(ticker: str, closes: pd.Series, source_url: str) -> None:
    CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    csv_path, meta_path = _cache_paths(ticker)
    out = closes.copy()
    out.index = pd.to_datetime(out.index).normalize()
    out = out[~out.index.duplicated(keep="last")].sort_index()
    pd.DataFrame({"date": out.index.strftime("%Y-%m-%d"), "close": out.to_numpy(dtype=float)}).to_csv(csv_path, index=False)
    meta = {
        "ticker": ticker,
        "source": "Yahoo Finance chart endpoint",
        "source_url": source_url,
        "retrieved_utc": datetime.utcnow().isoformat() + "Z",
        "rows": int(len(out)),
        "last_date": str(out.index.max().date()) if len(out) else None,
    }
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")


def fetch_yahoo_daily(ticker: str, years: int = 5) -> pd.Series:
    cached = _read_daily_cache(ticker)
    today = pd.Timestamp.now(tz=IST).normalize().tz_localize(None)
    if cached is not None and not cached.empty and cached.index.max() >= today - pd.Timedelta(days=1):
        return cached

    end = int(datetime.now().timestamp())
    start = int((datetime.now() - timedelta(days=365 * years)).timestamp())
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    r = requests.get(
        url,
        params={"period1": start, "period2": end, "interval": "1d", "events": "history"},
        timeout=20,
    )
    r.raise_for_status()
    payload = r.json()["chart"]["result"][0]
    dates = pd.to_datetime(payload["timestamp"], unit="s", utc=True).tz_convert(IST).tz_localize(None).normalize()
    closes = pd.Series(
        payload["indicators"]["quote"][0]["close"],
        index=dates,
        name="close",
        dtype="float64",
    ).dropna()
    closes = closes[~closes.index.duplicated(keep="last")].sort_index()
    _write_daily_cache(ticker, closes, url)
    return closes


def fetch_nse_chain() -> tuple[pd.DataFrame, dict[str, Any]]:
    s = _session()
    try:
        s.get(NSE_HOME, timeout=10)
        r = s.get(NSE_URL, timeout=15)
        r.raise_for_status()
        data = r.json()
    except Exception:
        r = s.get(NSE_URL, timeout=15)
        r.raise_for_status()
        data = r.json()

    rows = []
    rec = data.get("records", {})
    for item in rec.get("data", []):
        strike = item.get("strikePrice")
        expiry = item.get("expiryDate")
        for typ in ("CE", "PE"):
            leg = item.get(typ) or {}
            rows.append({
                "strike": strike,
                "expiry": expiry,
                "option_type": typ,
                "ltp": leg.get("lastPrice"),
                "bid": leg.get("bidprice"),
                "ask": leg.get("askPrice"),
                "volume": leg.get("totalTradedVolume"),
                "oi": leg.get("openInterest"),
            })
    if not rows:
        raise ValueError("NSE option chain returned no rows")
    meta = {
        "source": "NSE_PUBLIC_OPTION_CHAIN",
        "expiry_dates": rec.get("expiryDates", []),
        "timestamp": rec.get("timestamp"),
    }
    return pd.DataFrame(rows), meta


def fetch_sensex_chain() -> tuple[pd.DataFrame, dict[str, Any]]:
    # Explicit normalized adapter remains an override for users who have a
    # broker/vendor feed. Otherwise use the online unofficial BSE adapter.
    url = os.environ.get("BSE_OPTION_CHAIN_URL", "").strip()
    if url:
        token = os.environ.get("PAYTM_MONEY_JWT_TOKEN", "").strip()
        headers = {"Accept": "application/json", "User-Agent": "BATMAN-Prospective-Validation/1.0"}
        if token:
            headers["x-jwt-token"] = token
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        data = r.json()
        rows = data.get("rows") if isinstance(data, dict) else data
        if not isinstance(rows, list):
            raise ValueError(
                "BSE_OPTION_CHAIN_URL must return a JSON list or {'rows': [...]} "
                "with strike/option_type/ltp/bid/ask/expiry"
            )
        meta = {
            "source": "CONFIGURED_SENSEX_CHAIN_ADAPTER",
            "url": url,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        return pd.DataFrame(rows), meta

    from .bse_online import fetch_sensex_chain_indiaopt
    return fetch_sensex_chain_indiaopt()


def live_chain(underlying: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    if underlying == "NIFTY":
        return fetch_nse_chain()
    if underlying == "SENSEX":
        return fetch_sensex_chain()
    raise ValueError(underlying)
