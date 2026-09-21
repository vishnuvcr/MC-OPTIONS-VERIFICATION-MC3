from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class MethodFingerprint:
    name: str
    observation_definition: str
    sampling_scheme: str
    return_space: str
    anchor: str
    rng: str


def operational_mc1_paths(
    s0: float,
    log_returns: np.ndarray,
    horizon: int,
    paths: int = 5000,
    seed: int = 756,
    window: int = 756,
) -> np.ndarray:
    """Reproduce the MC1-lineage path transformation; not external-authority proof."""
    if s0 <= 0:
        raise ValueError("s0 must be positive")
    if horizon <= 0 or paths <= 0:
        raise ValueError("horizon and paths must be positive")
    x = np.asarray(log_returns, dtype=float)
    x = x[np.isfinite(x)]
    if x.size < window:
        raise ValueError(f"need at least {window} finite log returns")
    x = x[-window:]
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, window, size=(paths, horizon))
    sampled = x[idx]
    return s0 * np.exp(sampled.sum(axis=1))


def contiguous_block_paths(
    s0: float,
    log_returns: np.ndarray,
    horizon: int,
    paths: int = 5000,
    seed: int = 756,
    block_length: int = 5,
) -> np.ndarray:
    """Candidate dependence-preserving bootstrap for Phase 2 sensitivity only."""
    if s0 <= 0:
        raise ValueError("s0 must be positive")
    if horizon <= 0 or paths <= 0:
        raise ValueError("horizon and paths must be positive")
    if block_length <= 0:
        raise ValueError("block_length must be positive")
    x = np.asarray(log_returns, dtype=float)
    x = x[np.isfinite(x)]
    if x.size < 756:
        raise ValueError("need at least 756 finite log returns")
    x = x[-756:]
    rng = np.random.default_rng(seed)
    out = np.empty((paths, horizon), dtype=float)
    n = x.size
    for p in range(paths):
        pos = 0
        while pos < horizon:
            start = int(rng.integers(0, n))
            take = min(block_length, horizon - pos)
            ix = (start + np.arange(take)) % n
            out[p, pos:pos + take] = x[ix]
            pos += take
    return s0 * np.exp(out.sum(axis=1))


def method_fingerprint(name: str, observation_definition: str, sampling_scheme: str, return_space: str, anchor: str, rng: str) -> MethodFingerprint:
    return MethodFingerprint(name, observation_definition, sampling_scheme, return_space, anchor, rng)
