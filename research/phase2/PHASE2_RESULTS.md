# Phase 2 Results — Exact Reconstruction

## Status

Completed for the predecessor implementation lineage.

## Reconstruction result

MC-RQ6-v1 reproduces the MC1 implementation algorithmically:
- last 756 daily log returns before D3;
- IID sampling with replacement for each future step;
- NumPy default_rng seed 756;
- three-step horizon;
- S0 times exp(sum sampled log returns);
- empirical P20/P35/P65/P80 terminal quantiles;
- nearest unique tradable-strike mapping.

## Deterministic identity fixture

A fixed synthetic 900-return fixture, S0 = 100, horizon = 3, 100 paths and seed = 756 produces terminal-array SHA-256 fingerprint:
6f64abfc0c9d6f9e4e65f52fb47c6f837f208f963cbf05871cb15db8c8626677

The fingerprint above is used only as a deterministic implementation test, not as evidence of original BATMAN data.

## Authority qualification

The predecessor implementation is now exactly reproducible. An independent external original BATMAN source matching this method has still not been located. Therefore MC-RQ6-v1 is the traceable project control, not a claim of external authorship.

## Consequence for RQ-6

Any difference between earlier results and an independently executed MC-RQ6-v1 run cannot be attributed to the Monte Carlo path transformation if the earlier run used the same MC1-lineage implementation. Any remaining discrepancy must be traced to data, timestamp, strike-grid, cost, or execution implementation.
