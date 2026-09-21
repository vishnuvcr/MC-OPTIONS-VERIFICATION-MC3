# RQ-6 Supplement

## S1. Exact implementation lineage

The Monte Carlo method was traced to the earliest MC1 Monte Carlo source commit rather than inferred from later refactors.

## S2. Candidate resampling taxonomy

The Phase 1 literature review distinguishes IID single-return bootstrap, without-replacement permutation, moving or contiguous block bootstrap, stationary bootstrap, contiguous multi-day forward-window sampling, and parametric Monte Carlo.

Only the IID single-return bootstrap is supported by the direct MC1 source-code lineage.

## S3. Why method identity matters

A dependence-preserving transformation would change the distribution of multi-day terminal returns even with the same marginal one-day return sample. Therefore the pre-RQ-6 sampler uncertainty was a genuine model uncertainty. After source recovery, it is resolved for the predecessor implementation.

## S4. Capital interpretation

MC-RQ6-v1 controls the stochastic terminal-distribution layer. It does not define exchange SPAN margin or broker upfront margin. Those are separate calculations requiring separate attributable source data.

## S5. Future reporting requirements

Every subsequent candidate study should record the exact MC-RQ6-v1 version, historical-return boundaries, seed, path count, terminal hash where practical, strike map, execution timestamp, slippage/cost assumptions, capital definition and out-of-sample split.
