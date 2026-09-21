from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from typing import Any

import pandas as pd
import requests


IST="Asia/Kolkata"
NSE_URL="https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
NSE_HOME="https://www.nseindia.com"


def _session() -> requests.Session:
    s=requests.Session()
    s.headers.update({
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
        "Accept":"application/json,text/plain,*/*",
        "Accept-Language":"en-US,en;q=0.8",
        "Referer":NSE_HOME+"/option-chain",
        "Connection":"keep-alive",
    })
    return s


def fetch_yahoo_daily(ticker: str, years: int = 5) -> pd.Series:
    end=int(datetime.now().timestamp())
    start=int((datetime.now()-timedelta(days=365*years)).timestamp())
    url=f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    r=requests.get(url,params={"period1":start,"period2":end,"interval":"1d","events":"history"},timeout=20)
    r.raise_for_status()
    payload=r.json()["chart"]["result"][0]
    dates=pd.to_datetime(payload["timestamp"],unit="s",utc=True).tz_convert(IST).tz_localize(None).normalize()
    closes=pd.Series(payload["indicators"]["quote"][0]["close"],index=dates,name="close",dtype="float64").dropna()
    return closes[~closes.index.duplicated(keep="last")].sort_index()


def fetch_nse_chain() -> tuple[pd.DataFrame,dict[str,Any]]:
    s=_session()
    try:
        s.get(NSE_HOME,timeout=10)
        r=s.get(NSE_URL,timeout=15)
        r.raise_for_status()
        data=r.json()
    except Exception:
        r=s.get("https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY",timeout=15)
        r.raise_for_status()
        data=r.json()

    rows=[]
    rec=data.get("records",{})
    for item in rec.get("data",[]):
        strike=item.get("strikePrice")
        expiry=item.get("expiryDate")
        for typ,key in (("CE","CE"),("PE","PE")):
            leg=item.get(key) or {}
            rows.append({
                "strike":strike,"expiry":expiry,"option_type":typ,
                "ltp":leg.get("lastPrice"),"bid":leg.get("bidprice"),
                "ask":leg.get("askPrice"),"volume":leg.get("totalTradedVolume"),
                "oi":leg.get("openInterest")
            })
    if not rows:
        raise ValueError("NSE option chain returned no rows")
    meta={"source":"NSE_PUBLIC_OPTION_CHAIN","expiry_dates":rec.get("expiryDates",[]),"timestamp":data.get("records",{}).get("timestamp")}
    return pd.DataFrame(rows),meta


def fetch_sensex_chain() -> tuple[pd.DataFrame,dict[str,Any]]:
    # A clean adapter boundary: use a user-supplied normalized JSON endpoint or an
    # authenticated provider. This avoids scraping undocumented BSE internals.
    url=os.environ.get("BSE_OPTION_CHAIN_URL","").strip()
    if not url:
        raise RuntimeError("SENSEX live option-chain adapter is not configured; set BSE_OPTION_CHAIN_URL")
    token=os.environ.get("PAYTM_MONEY_JWT_TOKEN","").strip()
    headers={"Accept":"application/json","User-Agent":"BATMAN-Prospective-Validation/1.0"}
    if token:
        headers["x-jwt-token"]=token
    r=requests.get(url,headers=headers,timeout=20)
    r.raise_for_status()
    data=r.json()
    rows=data.get("rows") if isinstance(data,dict) else data
    if not isinstance(rows,list):
        raise ValueError("BSE_OPTION_CHAIN_URL must return a JSON list or {'rows': [...]} with strike/option_type/ltp/bid/ask/expiry")
    meta={"source":"CONFIGURED_SENSEX_CHAIN_ADAPTER","url":url,"timestamp":datetime.utcnow().isoformat()+"Z"}
    return pd.DataFrame(rows),meta


def live_chain(underlying: str) -> tuple[pd.DataFrame,dict[str,Any]]:
    if underlying=="NIFTY":
        return fetch_nse_chain()
    if underlying=="SENSEX":
        return fetch_sensex_chain()
    raise ValueError(underlying)
