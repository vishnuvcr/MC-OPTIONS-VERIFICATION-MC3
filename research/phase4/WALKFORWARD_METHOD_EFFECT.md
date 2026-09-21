# Phase 4 — Walk-Forward Method-Effect Revalidation

The inherited MC2 baseline had 97 valid expiries and 52 gross-MC-EV-gated trades. Mean net P&L per gated trade was 1727.24 and the ES99 proxy was 12706.60.

The prior in-sample frontier was P22/P33/P67/P78 with an ES99 proxy of 12130.41, about 4.53% below the prior baseline.

Prior walk-forward records:
- Split A selected P20.5/P35/P65/P79.5; 2026 common-gated delta was -161.18, CI [-818.18, 334.65], sign-flip p=1.00.
- Split B selected P22/P33/P67/P78; 2026 common-gated delta was +266.12, CI [-914.74, 1270.04], sign-flip p=0.643.

RQ-6 finding: MC-RQ6-v1 is algorithmically identical to the earliest MC1 sampler. Therefore, conditional on the inherited MC2 results using that same sampler, the strike frontier and walk-forward outcomes are method-invariant.

MC3 does not contain the MC2 raw option cache, so this is a conditional method-equivalence result, not a new independent 97-expiry backtest.

No actual NSE or Paytm Money margin reduction is established by RQ-6. Earlier ES99 and stress-loss values remain capital proxies.