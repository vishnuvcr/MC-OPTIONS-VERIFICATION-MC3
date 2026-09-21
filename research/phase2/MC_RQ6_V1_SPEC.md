# MC-RQ6-v1 — Traceable Monte Carlo Control Specification

## Provenance status

This is the exact Monte Carlo control reconstructed from the earliest MC1 project implementation. It is authoritative for reproducing the predecessor project implementation, but external originality of the BATMAN method remains unverified.

## Observation set

For each D3 signal date, keep daily observations strictly before D3, compute adjacent daily log returns, drop non-finite values, and retain the final 756 finite returns. This normally requires 757 daily closes.

## Horizon

The expiry session tuple is D3 signal, D2, D1, expiry. The MC horizon is therefore 3 daily-return steps.

## Sampler

For each future step, draw an integer index uniformly from the 756 historical returns with replacement using NumPy default_rng(seed=756). No block dependence or without-replacement permutation is imposed.

## Transformation

S_T = S_0 * exp(sum of the sampled log returns).

## D3 09:30 anchor

Use the latest option observation at or before 09:30 IST. Prefer the median call-put-parity estimate K + CE - PE for strikes within 2% of the previous close; use previous close only as fallback.

## Terminal quantiles

Compute empirical terminal-spot quantiles at 0.20, 0.35, 0.65 and 0.80.

## Strike map

Map to the nearest available strike on the correct PE or CE side, ensure all four selected strikes are unique, and resolve ties to the lower strike.

## Locked portfolio

+1 P35 PE; -2 P20 PE; +1 P65 CE; -2 P80 CE.

## Identity rule

A claimed MC-RQ6-v1 implementation must match the observation vector, seed, horizon, starting spot and terminal-array fingerprint for a fixed test fixture.