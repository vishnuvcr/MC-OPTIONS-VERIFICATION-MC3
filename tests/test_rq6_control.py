import hashlib
import numpy as np
from src.rq6.control import simulate_terminal_paths

def test_mc_rq6_v1_fixture_hash():
    r = np.tile(np.array([0.01, -0.005, 0.002]), 300)
    out = simulate_terminal_paths(100.0, r, horizon=3, paths=100, seed=756)
    got = hashlib.sha256(out.tobytes()).hexdigest()
    assert got == "6f64abfc0c9d6f9e4e65f52fb47c6f837f208f963cbf05871cb15db8c8626677"
