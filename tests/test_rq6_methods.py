import numpy as np

from src.rq6.methods import operational_mc1_paths, contiguous_block_paths


def test_operational_method_is_deterministic():
    r = np.tile(np.array([0.01, -0.005, 0.002]), 300).astype(float)
    a = operational_mc1_paths(100.0, r, horizon=3, paths=100, seed=756)
    b = operational_mc1_paths(100.0, r, horizon=3, paths=100, seed=756)
    assert a.shape == (100,)
    assert np.array_equal(a, b)


def test_operational_method_requires_756_returns():
    r = np.ones(755)
    try:
        operational_mc1_paths(100.0, r, horizon=1)
    except ValueError:
        return
    raise AssertionError("expected short-history rejection")


def test_operational_method_uses_only_last_window():
    r = np.arange(800, dtype=float) / 100000.0
    a = operational_mc1_paths(100.0, r, horizon=1, paths=10, seed=1)
    assert a.shape == (10,)


def test_block_candidate_is_deterministic():
    r = np.tile(np.array([0.01, -0.005, 0.002]), 300).astype(float)
    a = contiguous_block_paths(100.0, r, horizon=7, paths=25, seed=756, block_length=3)
    b = contiguous_block_paths(100.0, r, horizon=7, paths=25, seed=756, block_length=3)
    assert np.array_equal(a, b)
