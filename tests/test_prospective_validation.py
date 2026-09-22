import numpy as np
import pandas as pd

from src.prospective_validation.core import (
    simulate_terminal_paths, choose_unique_strikes, portfolio_mc_ev,
    entry_price, mark_price, is_d3
)


def test_mc_deterministic_shape():
    r=np.tile(np.array([0.01,-0.005,0.002]),300)
    out=simulate_terminal_paths(100,r,horizon=3,paths=100,seed=756)
    assert out.shape==(100,)
    assert np.isfinite(out).all()


def test_unique_strikes_lower_tie_break():
    chain=pd.DataFrame([
        {"strike":95,"option_type":"PE","ltp":1.0},
        {"strike":100,"option_type":"PE","ltp":1.0},
        {"strike":110,"option_type":"PE","ltp":1.0},
        {"strike":115,"option_type":"PE","ltp":1.0},
        {"strike":95,"option_type":"CE","ltp":1.0},
        {"strike":100,"option_type":"CE","ltp":1.0},
        {"strike":110,"option_type":"CE","ltp":1.0},
        {"strike":115,"option_type":"CE","ltp":1.0},
    ])
    got=choose_unique_strikes(chain,{"P20_PE":105,"P35_PE":105,"P65_CE":105,"P80_CE":105})
    assert got["P20_PE"]==100
    assert got["P35_PE"]==110


def test_entry_and_mark_conventions():
    from src.prospective_validation.core import LegQuote
    px,src=entry_price(LegQuote(99,101,100),1,2)
    assert px==103 and src=="ask_plus_slippage"
    px,src=entry_price(LegQuote(99,101,100),-1,2)
    assert px==97 and src=="bid_minus_slippage"
    px,src=mark_price(LegQuote(99,101,100),1)
    assert px==99 and src=="bid"
    px,src=mark_price(LegQuote(99,101,100),-1)
    assert px==101 and src=="ask"


def test_d3_definition():
    h=set()
    assert is_d3(pd.Timestamp("2026-09-29").date(),pd.Timestamp("2026-10-02").date(),h)
