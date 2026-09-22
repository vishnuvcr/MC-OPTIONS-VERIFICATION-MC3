from __future__ import annotations

import os
import pandas as pd


def brokerage_per_order(trade_date: pd.Timestamp) -> float:
    # Prospective paper validation default. Override with
    # PAYTM_MONEY_BROKERAGE_PER_ORDER when the account-specific current rate
    # is verified. The dashboard records the configured amount.
    return float(os.environ.get("PAYTM_MONEY_BROKERAGE_PER_ORDER", "20.0"))


def stt_sale_rate(trade_date: pd.Timestamp) -> float:
    d = pd.Timestamp(trade_date).date()
    if d < pd.Timestamp("2024-10-01").date():
        return 0.000625
    if d < pd.Timestamp("2026-04-01").date():
        return 0.001
    return 0.0015


def stt_exercise_rate(trade_date: pd.Timestamp) -> float:
    d = pd.Timestamp(trade_date).date()
    if d < pd.Timestamp("2026-04-01").date():
        return 0.00125
    return 0.0015


def exchange_transaction_rate_per_crore(underlying: str, trade_date: pd.Timestamp) -> float:
    d = pd.Timestamp(trade_date).date()
    if d < pd.Timestamp("2024-10-01").date():
        raise ValueError("enhanced exchange transaction schedule is not defined before 2024-10-01")
    if underlying == "NIFTY":
        # NSE revision effective 1-Mar-2026 kept total member outflow at Rs 3,553/cr.
        return 3553.0
    if underlying == "SENSEX":
        # Locked inherited BSE research schedule. Update only after attributable
        # current BSE charge evidence is added to the provider audit.
        return 3250.0
    raise ValueError(underlying)


def enhanced_entry_costs(
    underlying: str,
    prices: dict[str, float],
    quantities: dict[str, int],
    lot_size: int,
    trade_date: pd.Timestamp,
) -> dict[str, float]:
    brokerage = 4.0 * brokerage_per_order(trade_date)
    premium_turnover = sum(abs(q) * abs(float(prices[label])) * lot_size for label, q in quantities.items())
    exchange_txn = exchange_transaction_rate_per_crore(underlying, trade_date) / 1e7 * premium_turnover
    sebi = 0.000001 * premium_turnover
    stamp = 0.00003 * sum(max(q, 0) * abs(float(prices[label])) * lot_size for label, q in quantities.items())
    gst = 0.18 * (brokerage + exchange_txn + sebi)
    stt_entry = sum(
        stt_sale_rate(trade_date) * abs(q) * abs(float(prices[label])) * lot_size
        for label, q in quantities.items() if q < 0
    )
    return {
        "brokerage": brokerage,
        "stt_entry": stt_entry,
        "exchange_transaction": exchange_txn,
        "sebi_turnover": sebi,
        "stamp_duty": stamp,
        "gst_on_brokerage_and_venue_fees": gst,
        "total_enhanced_entry_cost": brokerage + exchange_txn + sebi + stamp + gst + stt_entry,
        "brokerage_per_order": brokerage_per_order(trade_date),
    }


def expiry_stt(
    expiry_date: pd.Timestamp,
    settlement_spot: float,
    strikes: dict[str, float],
    quantities: dict[str, int],
    lot_size: int,
) -> float:
    rate = stt_exercise_rate(expiry_date)
    total = 0.0
    for label, q in quantities.items():
        if q <= 0:
            continue
        k = float(strikes[label])
        intrinsic = max(k - settlement_spot, 0.0) if label.endswith("PE") else max(settlement_spot - k, 0.0)
        total += rate * q * intrinsic * lot_size
    return total
