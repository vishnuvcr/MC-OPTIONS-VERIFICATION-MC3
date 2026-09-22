import pandas as pd
from src.prospective_validation.core import choose_unique_strikes, LegQuote, entry_price, mark_price

def main() -> None:
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
    print("chosen", got)
    assert got["P20_PE"] == 100
    assert got["P35_PE"] == 110

    q = LegQuote(99, 101, 100)
    assert entry_price(q, 1, 2) == (103.0, "ask_plus_slippage")
    assert entry_price(q, -1, 2) == (97.0, "bid_minus_slippage")
    assert mark_price(q, 1) == (99.0, "bid")
    assert mark_price(q, -1) == (101.0, "ask")
    print("strike/execution smoke PASS")

if __name__ == "__main__":
    main()
