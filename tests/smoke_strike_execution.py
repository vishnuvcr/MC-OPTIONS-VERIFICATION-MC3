import math
import pandas as pd

from src.prospective_validation.core import choose_unique_strikes, LegQuote, entry_price, mark_price


def main() -> None:
    chain = pd.DataFrame([
        {"strike": 95, "option_type": "PE", "ltp": 1.0},
        {"strike": 100, "option_type": "PE", "ltp": 1.0},
        {"strike": 110, "option_type": "PE", "ltp": 1.0},
        {"strike": 115, "option_type": "PE", "ltp": 1.0},
        {"strike": 95, "option_type": "CE", "ltp": 1.0},
        {"strike": 100, "option_type": "CE", "ltp": 1.0},
        {"strike": 110, "option_type": "CE", "ltp": 1.0},
        {"strike": 115, "option_type": "CE", "ltp": 1.0},
    ])
    got = choose_unique_strikes(
        chain,
        {"P20_PE": 105, "P35_PE": 105, "P65_CE": 105, "P80_CE": 105},
    )
    assert set(got) == {"P20_PE", "P35_PE", "P65_CE", "P80_CE"}
    assert len(set(got.values())) == 4
    assert 100.0 in (got["P20_PE"], got["P35_PE"])
    assert 95.0 in (got["P65_CE"], got["P80_CE"])
    assert all(isinstance(v, float) for v in got.values())

    q = LegQuote(99, 101, 100)
    long_entry, long_src = entry_price(q, 1, 2)
    short_entry, short_src = entry_price(q, -1, 2)
    long_mark, long_mark_src = mark_price(q, 1)
    short_mark, short_mark_src = mark_price(q, -1)

    assert math.isclose(long_entry, 103.0)
    assert math.isclose(short_entry, 97.0)
    assert long_src == "ask_plus_slippage"
    assert short_src == "bid_minus_slippage"
    assert math.isclose(long_mark, 99.0)
    assert math.isclose(short_mark, 101.0)
    assert long_mark_src == "bid"
    assert short_mark_src == "ask"
    print("strike/execution smoke PASS")


if __name__ == "__main__":
    main()
