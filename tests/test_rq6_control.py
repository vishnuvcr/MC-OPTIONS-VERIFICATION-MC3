import hashlib
import numpy as np
import pandas as pd

from src.rq6.control import historical_log_returns, simulate_terminal_paths, terminal_quantiles


def test_fixed_terminal_array_fingerprint():
    r = np.tile(np.array([0.01, -0.005, 0.002]), 300).astype(float)
    out = simulate_terminal_paths(100.0, r, horizon=3, paths=100, seed=756)
    assert hashlib.sha256(out.tobytes()).hexdigest() == "6f64abfc0c9d6f9e4e65f52fb47c6f837f208f963cbf05871cb15db8c8626677"


def test_historical_window_has_756_returns_before_signal():
    dates = pd.date_range("2020-01-01", periods=760, freq="D")
    closes = np.exp(np.linspace(0, 1, len(dates)))
    daily = pd.DataFrame({"date": dates, "close": closes})
    r = historical_log_returns(daily, dates[-1], window=756)
    assert len(r) == 756


def test_terminal_quantile_labels():
    q = terminal_quantiles(np.arange(100.0))
    assert set(q) == {"P20_PE", "P35_PE", "P65_CE", "P80_CE"}
