# RQ-6 External Source Audit

## Purpose

Test whether a public source outside the predecessor repository defines the exact BATMAN Monte Carlo transformation.

## Sources reviewed

### OpenAlgo
https://openalgo.in/options-strategies/advanced-multileg

The current OpenAlgo Batman description is a four-leg ratio structure with concrete strikes for a 2026 expiry. It does not specify the RQ-6 756-session Monte Carlo, D3 09:30 anchor, P20/P35/P65/P80 terminal quantiles or the MC1 RNG transformation.

### TradeJini / NxtOption
https://www.tradejini.com/blogs/how-to-trade-the-batman-strategy-using-nxtoption

Published 2 September 2026. The article defines Batman generically as a two-sided ratio trade and discusses directional-neutral positioning and expiry payoff. It does not provide the RQ-6 Monte Carlo specification.

### Alice Blue / The Trading Scholar YouTube session
https://youtube.com/live/duDHc76X7KY

The public announcement describes a Batman options strategy session. The accessible summary of the recorded session gives different timing and strike-selection rules, including monthly-expiry positioning and fixed point distances. It is not evidence for the MC1/RQ-6 transformation.

### YouTube summary of the same session
https://videohighlight.com/v/duDHc76X7KY

The summary records a last-Friday-before-monthly-expiry entry around 15:16 and point-distance examples for NIFTY strikes. These rules differ from the MC1 D3/09:30, terminal-quantile approach.

### Suresh Kumar public Batman thread
https://en.rattibha.com/thread/1608802286079467526

The 2022 thread describes Batman as a combination of two call/put ratio spreads and selects strikes using premium relationships. It does not describe a 756-session Monte Carlo or the RQ-6 quantile method.

### DTBhat public Batman thread/video reference
https://en.rattibha.com/thread/1715730751956877479

A BankNifty example using a Batman structure is described, again without the RQ-6 Monte Carlo specification.

## Audit conclusion

The public sources above establish that the term Batman is not a unique algorithmic definition. They are useful contextual sources but cannot override direct MC1 source-code lineage.

The exact RQ-6 signature was not found in the reviewed public material:
- 756 pre-D3 historical log returns;
- IID with-replacement sampling using default_rng(756);
- three-step D3-to-expiry path;
- D3 09:30 parity-derived S0;
- P20/P35/P65/P80 terminal quantiles;
- nearest unique listed-strike mapping;
- +1/-2/+1/-2 locked legs.

Therefore the authority hierarchy remains: direct MC1 lineage for implementation reproducibility; external-original BATMAN authority unresolved.
