from __future__ import annotations

import asyncio
import importlib.metadata
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


def normalize_indiaopt_result(result: Any, scrip: str = SENSEX_SCRIP) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Convert indiaopt BSEClient output into the prospective engine schema.

    indiaopt exposes one row per strike with call/put fields. The package's
    current public examples expose LTP/OI/volume and an expiry at the result
    level; bid/ask are optional and therefore remain nullable.
    """
    rows = list(_field(result, "data") or [])
    if not rows:
        raise ValueError("indiaopt returned an empty SENSEX option chain")

    expiry = _field(result, "expiry")
    spot = _field(result, "spot_price")
    fetched_at = _field(result, "fetched_at")

    normalized: list[dict[str, Any]] = []
    for row in rows:
        strike = _field(row, "strike")
        if strike is None:
            continue
        for option_type, prefix in (("CE", "call"), ("PE", "put")):
            ltp = _field(row, f"{prefix}_ltp", f"{prefix}_last_price")
            normalized.append({
                "strike": strike,
                "expiry": expiry,
                "option_type": option_type,
                "ltp": ltp,
                "bid": _field(row, f"{prefix}_bid", f"{prefix}_bid_price"),
                "ask": _field(row, f"{prefix}_ask", f"{prefix}_offer_price", f"{prefix}_offer"),
                "volume": _field(row, f"{prefix}_vol", f"{prefix}_volume"),
                "oi": _field(row, f"{prefix}_oi", f"{prefix}_open_interest"),
            })

    out = pd.DataFrame(normalized)
    if out.empty:
        raise ValueError("indiaopt SENSEX result contained no strike rows")
    out["expiry"] = pd.to_datetime(out["expiry"], errors="coerce").dt.normalize()
    for col in ("strike", "ltp", "bid", "ask", "volume", "oi"):
        out[col] = pd.to_numeric(out[col], errors="coerce")
    out = out.dropna(subset=["strike", "ltp"])
    if out.empty:
        raise ValueError("indiaopt SENSEX result contained no usable option prices")

    try:
        package_version = importlib.metadata.version("indiaopt")
    except importlib.metadata.PackageNotFoundError:
        package_version = "unknown"

    meta = {
        "source": "UNOFFICIAL_INDIAOPT_BSE",
        "provider": "indiaopt",
        "provider_version": package_version,
        "exchange": "BSE",
        "scrip": str(scrip),
        "expiry": str(expiry) if expiry is not None else None,
        "spot_price": float(spot) if spot is not None else None,
        "fetched_at": str(fetched_at) if fetched_at is not None else None,
        "retrieved_utc": datetime.utcnow().isoformat() + "Z",
        "provenance": "unofficial_public_package_using_BSE_market_data_endpoints",
        "bid_ask_note": "indiaopt public result may expose LTP/OI/volume without bid/ask; engine falls back to LTP with locked slippage.",
    }
    return out, meta


async def _fetch_async(settings: Any) -> tuple[pd.DataFrame, dict[str, Any]]:
    from indiaopt import BSEClient

    async with BSEClient(settings=settings) as client:
        result = await client.fetch_option_chain(SENSEX_SCRIP, is_index=True)
    return normalize_indiaopt_result(result)


def fetch_sensex_chain_indiaopt() -> tuple[pd.DataFrame, dict[str, Any]]:
    """Fetch SENSEX online using the unofficial indiaopt BSE adapter."""
    try:
        from indiaopt import Settings
    except ImportError as exc:
        raise RuntimeError("indiaopt is not installed") from exc

    settings = Settings(
        max_retries=3,
        fetch_timeout=15.0,
        log_level="WARNING",
    )
    return asyncio.run(_fetch_async(settings))
