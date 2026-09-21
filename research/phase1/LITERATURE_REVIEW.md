# Phase 1 Literature Review — Historical-Return Monte Carlo and Time-Series Resampling

## Scope

This literature review is limited to methods that can distinguish among the plausible BATMAN path-generation mechanisms. It is not used as evidence that BATMAN used any particular method.

## Monte Carlo option methods

Boyle's classic Monte Carlo option-pricing paper frames the problem as simulating the process generating underlying returns and evaluating option values from simulated outcomes. The key methodological point for RQ-6 is that Monte Carlo is a family of path-generation choices rather than one unique algorithm.

Reference: Boyle, P. (1977), Options: A Monte Carlo approach, Journal of Financial Economics, 4(3), 323-338. DOI 10.1016/0304-405X(77)90005-8.

## Historical-return simulation

Canonical least-squares Monte Carlo work explicitly describes sampling future gross returns independently from a historical return set to create simulated price paths. This is structurally close to the MC1 operational implementation: a historical return set, random future draws and a compounded path.

Reference: Liu, Q. (2008), Pricing American Options by Canonical Least-Squares Monte Carlo, SSRN 1145331. Later empirical work describes independent historical gross-return draws and the resulting price-path construction.

## Dependence-preserving resampling

The time-series bootstrap literature distinguishes IID single-observation resampling from methods designed for dependent observations. Kunsch's moving-block bootstrap preserves short-lag dependence by resampling contiguous blocks. Politis and Romano's stationary bootstrap extends this idea to weakly dependent stationary series using random blocks. This matters because volatility clustering and serial dependence can change the distribution of multi-step terminal outcomes.

References:
- Kunsch, H. (1989), The Jackknife and the Bootstrap for General Stationary Observations.
- Politis, D.N. & Romano, J.P. (1994), The Stationary Bootstrap, JASA 89(428), 1303-1313. DOI 10.1080/01621459.1994.10476870.

## Implication for RQ-6

The current MC1 implementation is not equivalent to a block bootstrap: each future day selects an individual historical log return independently with replacement. Therefore, if the original BATMAN implementation instead preserved return dependence, RQ-6 could materially alter terminal quantiles even with the same 756 historical observations and 5,000 paths.

Conversely, if an authoritative source shows independent historical-return draws, then the current MC1 sampler is methodologically aligned and the remaining RQ-6 risk moves to observation boundary, anchor and implementation details rather than sampling dependence.

## D3 09:30 and information-set integrity

The initial condition must be treated separately from the historical-return sampler. Using an option snapshot at or before 09:30 and deriving an implied spot is a different model from anchoring directly to the previous close or to a later intraday index value. The distinction is critical for avoiding look-ahead and for reproducing the exact terminal distribution.

## Tradable strike mapping

A continuous terminal quantile is not itself a tradable contract. NSE documents discrete NIFTY index-option strike intervals and expiry rules; therefore any reproducible strategy must specify both the model quantile and the strike-grid mapping rule.

## Literature-based candidate taxonomy

RQ-6 therefore treats these as scientifically distinct candidate mechanisms:
1. IID single-return bootstrap with replacement.
2. Without-replacement permutation of individual returns.
3. Moving/contiguous block bootstrap.
4. Stationary bootstrap.
5. Historical contiguous multi-day forward-window sampling.
6. Parametric Monte Carlo fit to return moments or a chosen stochastic process.

Only source evidence can promote one candidate to authoritative BATMAN method.
