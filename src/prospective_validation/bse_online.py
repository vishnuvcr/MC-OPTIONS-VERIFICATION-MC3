from __future__ import annotations

import asyncio
import importlib
import importlib.metadata
import inspect
from datetime import datetime
from typing import Any

import pandas as pd


SENSEX_SCRIP = "999920"


def _field(obj: Any, *names: str) -> Any:
    for name in names:
        if isinstance(obj, dict) and name in obj:
            return obj[name]
        if hasattr(obj, name):
            return getattr(obj, name)
    return None


def _version(package: str) -> str:
    try:
        return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


def _normalise_records(rows: Any, expiry: Any = None) -> list[dict[str, Any]]:
    if isinstance(rows, dict):
        for key in ("data", "records", "filtered", "option_chain", "chain", "rows"):
            if key in rows:
                nested = rows[key]
                if isinstance(nested, dict) and key == "filtered":
                    nested = nested.get("data", nested)
                return _normalise_records(nested, expiry or rows.get("expiry"))
        # A single strike record can itself be a mapping.
        if "strikePrice" in rows or "strike" in rows:
            return [rows]
        return []

    if not isinstance(rows, (list, tuple)):
        return []

    out: list[dict[str, Any]] = []
    for row in rows:
        if isinstance(row, dict):
            strike = _field(row, "strikePrice", "strike", "strike_price")
            if strike is not None:
                ce = _field(row, "CE", "ce", "call", "CALL") or {}
                pe = _field(row, "PE", "pe", "put", "PUT") or {}
                for typ, leg in (("CE", ce), ("PE", pe)):
                    if not isinstance(leg, dict):
                        leg = {}
                    out.append({
                        "strike": strike,
                        "expiry": _field(leg, "expiryDate", "expiry", "expiry_date") or expiry,
                        "option_type": typ,
                        "ltp": _field(leg, "lastPrice", "ltp", "last_price"),
                        "bid": _field(leg, "bid", "bidPrice", "bid_price"),
                        "ask": _field(leg, "ask", "askPrice", "ask_price"),
                        "volume": _field(leg, "volume", "totalTradedVolume", "total_traded_volume"),
                        "oi": _field(leg, "openInterest", "oi", "open_interest"),
                    })
            else:
                # Already one-leg-per-row schemas.
                typ = str(_field(row, "option_type", "optionType", "type") or "").upper()
                if typ in ("CE", "PE"):
                    out.append({
                        "strike": _field(row, "strikePrice", "strike", "strike_price"),
                        "expiry": _field(row, "expiryDate", "expiry", "expiry_date") or expiry,
                        "option_type": typ,
                        "ltp": _field(row, "lastPrice", "ltp", "last_price"),
                        "bid": _field(row, "bid", "bidPrice", "bid_price"),
                        "ask": _field(row, "ask", "askPrice", "ask_price"),
                        "volume": _field(row, "volume", "totalTradedVolume", "total_traded_volume"),
                        "oi": _field(row, "openInterest", "oi", "open_interest"),
                    })
    return out


def _normalise_payload(payload: Any, source: str, provider: str, scrip: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    expiry = _field(payload, "expiry", "expiryDate", "selected_expiry")
    spot = _field(payload, "spot_price", "spotPrice", "underlyingValue", "underlying_value")
    fetched_at = _field(payload, "fetched_at", "timestamp", "lastUpdateTime")
    rows = _normalise_records(payload, expiry)
    if not rows:
        raise ValueError(f"{provider} returned no recognisable SENSEX option rows")

    out = pd.DataFrame(rows)
    out["expiry"] = pd.to_datetime(out["expiry"], errors="coerce").dt.normalize()
    for col in ("strike", "ltp", "bid", "ask", "volume", "oi"):
        out[col] = pd.to_numeric(out[col], errors="coerce")
    out = out.dropna(subset=["strike", "ltp"])
    out = out[out["option_type"].isin(["CE", "PE"])]
    if out.empty:
        raise ValueError(f"{provider} returned no usable SENSEX option prices")

    meta = {
        "source": source,
        "provider": provider,
        "provider_version": _version(provider),
        "exchange": "BSE",
        "scrip": str(scrip),
        "expiry": str(expiry) if expiry is not None else None,
        "spot_price": float(spot) if spot is not None else None,
        "fetched_at": str(fetched_at) if fetched_at is not None else None,
        "retrieved_utc": datetime.utcnow().isoformat() + "Z",
        "provenance": "unofficial_public_package_using_BSE_market_data_endpoints",
    }
    return out, meta


async def _indiaopt_fetch(underlying: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    from indiaopt import BSEClient, NSEClient, Settings

    settings = Settings(max_retries=4, fetch_timeout=20.0, log_level="WARNING")
    if underlying == "NIFTY":
        async with NSEClient(settings=settings) as client:
            result = await client.fetch_option_chain("NIFTY")
        return _normalise_payload(result, "UNOFFICIAL_INDIAOPT_NSE", "indiaopt", "NIFTY")

    async with BSEClient(settings=settings) as client:
        result = await client.fetch_option_chain(SENSEX_SCRIP, is_index=True)
    return _normalise_payload(result, "UNOFFICIAL_INDIAOPT_BSE", "indiaopt", SENSEX_SCRIP)


def _call_compatible(fn: Any, scrip: str) -> Any:
    sig = inspect.signature(fn)
    params = list(sig.parameters.values())
    kwargs: dict[str, Any] = {}
    for p in params:
        if p.name in ("scrip_cd", "scrip_code", "scrip", "symbol", "symbol_code"):
            kwargs[p.name] = scrip
        elif p.default is inspect.Parameter.empty and p.kind in (
            inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD
        ):
            # The first required positional parameter is normally the symbol/scrip.
            if not kwargs:
                return fn(scrip)
    return fn(**kwargs)


def _bse_options_fetch() -> tuple[pd.DataFrame, dict[str, Any]]:
    """Best-effort adapter for the separate unofficial bse-options package.

    The package is intentionally treated as an opaque third-party integration:
    discover its public chain/expiry callable at runtime rather than depending
    on undocumented internals. If the package shape changes, this path fails
    closed and the error is retained.
    """
    mod = importlib.import_module("bse_options")
    names = [n for n in dir(mod) if not n.startswith("_")]
    candidates: list[tuple[int, str, Any]] = []
    for name in names:
        obj = getattr(mod, name)
        if callable(obj):
            low = name.lower()
            if "chain" in low:
                score = 0
                if "option" in low:
                    score += 3
                if "fetch" in low or "get" in low:
                    score += 2
                candidates.append((score, name, obj))
    candidates.sort(reverse=True, key=lambda x: x[0])

    errors: list[str] = []
    for _, name, fn in candidates:
        try:
            payload = _call_compatible(fn, SENSEX_SCRIP)
            if inspect.isawaitable(payload):
                payload = asyncio.run(payload)
            chain, meta = _normalise_payload(
                payload, "UNOFFICIAL_BSE_OPTIONS", "bse-options", SENSEX_SCRIP
            )
            meta["adapter_callable"] = name
            return chain, meta
        except Exception as exc:
            errors.append(f"{name}: {type(exc).__name__}: {exc}")

    raise RuntimeError("bse-options fallback could not produce a usable chain; " + " | ".join(errors[:5]))


def fetch_nifty_chain() -> tuple[pd.DataFrame, dict[str, Any]]:
    try:
        return asyncio.run(_indiaopt_fetch("NIFTY"))
    except Exception as exc:
        raise RuntimeError(f"indiaopt NIFTY provider failed: {type(exc).__name__}: {exc}") from exc


def fetch_sensex_chain() -> tuple[pd.DataFrame, dict[str, Any]]:
    try:
        return asyncio.run(_indiaopt_fetch("SENSEX"))
    except Exception as first:
        try:
            return _bse_options_fetch()
        except Exception as second:
            raise RuntimeError(
                "All unofficial SENSEX providers failed. "
                f"indiaopt={type(first).__name__}: {first}; "
                f"bse-options={type(second).__name__}: {second}"
            ) from second
