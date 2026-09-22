from datetime import date
import numpy as np
import pandas as pd

from src.prospective_validation.core import (
    LegQuote,
    choose_unique_strikes,
    entry_price,
    is_d3,
    mark_price,
    simulate_terminal_paths,
)
from src.prospective_validation.site import build as build_site
from src.prospective_validation.engine import scan, mark


def main() -> None:
    r = np.tile(np.array([0.01, -0.005, 0.002]), 300)
    out = simulate_terminal_paths(100.0, r, horizon=3, paths=100, seed=756)
    assert out.shape == (100,)
    assert np.isfinite(out).all()

    chain = pd.DataFrame([
        {"strike": 100, "option_type": "PE", "ltp": 1.0},
        {"strike": 110, "option_type": "PE", "ltp": 1.0},
        {"strike": 100, "option_type": "CE", "ltp": 1.0},
        {"strike": 110, "option_type": "CE", "ltp": 1.0},
    ])
    got = choose_unique_strikes(
        chain,
        {"P20_PE": 105, "P35_PE": 105, "P65_CE": 105, "P80_CE": 105},
    )
    assert got["P20_PE"] == 100
    assert got["P35_PE"] == 110

    q = LegQuote(99, 101, 100)
    assert entry_price(q, 1, 2) == (103, "ask_plus_slippage")
    assert entry_price(q, -1, 2) == (97, "bid_minus_slippage")
    assert mark_price(q, 1) == (99, "bid")
    assert mark_price(q, -1) == (101, "ask")

    assert is_d3(date(2026, 9, 29), date(2026, 10, 2), set())

    # Smoke-test the actual page generator with empty/initial ledgers.
    build_site()

    assert callable(scan)
    assert callable(mark)

    print("BATMAN prospective validation smoke test: PASS")


if __name__ == "__main__":
    main()
