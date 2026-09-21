from __future__ import annotations

import numpy as np
import pandas as pd


def historical_log_returns(daily: pd.DataFrame, signal_date: pd.Timestamp, window: int = 756) -> np.ndarray:
    d = daily[daily["date"] < pd.Timestamp(signal_date)].copy()
    d["close"] = pd.to_numeric(d["close"], errors="coerce")
    d["logret"] = np.log(d["close"].astype(float)).diff()
    return d["logret"].dropna().to_numpy(dtype=float)[-window:]


def simulate_terminal_paths(
    s0: float,
    historical_log_returns: np.ndarray,
    horizon: int = 3,
    paths: int = 5000,
    seed: int = 756,
    window: int = 756,
) -> np.ndarray:
    if s0 <= 0:
        raise ValueError("s0 must be positive")
    if horizon <= 0:
        raise ValueError("horizon must be positive")
    hist = np.asarray(historical_log_returns, dtype=float)
    hist = hist[np.isfinite(hist)]
    if hist.size < window:
        raise ValueError(f"need >={window} historical returns, got {hist.size}")
    hist = hist[-window:]
    rng = np.random.default_rng(seed)
    sample_idx = rng.integers(0, hist.size, size=(paths, horizon))
    sampled = hist[sample_idx]
    return s0 * np.exp(sampled.sum(axis=1))


def terminal_quantiles(terminals: np.ndarray) -> dict[str, float]:
    return {
        "P20_PE": float(np.quantile(terminals, 0.20)),
        "P35_PE": float(np.quantile(terminals, 0.35)),
        "P65_CE": float(np.quantile(terminals, 0.65)),
        "P80_CE": float(np.quantile(terminals, 0.80)),
    }
