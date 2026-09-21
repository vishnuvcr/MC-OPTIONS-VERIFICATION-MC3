# Phase 3 — Baseline Method-Effect Revalidation

## RQ-6 purpose

Determine whether replacing the predecessor operational MC implementation with MC-RQ6-v1 changes baseline gate decisions, terminal strikes, gross MC-EV or downstream realized economics.

## Identity result

MC-RQ6-v1 is algorithmically identical to the earliest MC1 Monte Carlo implementation. Under identical inputs, the same ordered 756-return vector, the same S0, the same three-step horizon, the same path count and the same seed produce the same terminal array.

Therefore the method-induced differences are exactly zero for any deterministic downstream calculation:

- terminal distribution: unchanged;
- P20/P35/P65/P80 targets: unchanged;
- selected strikes: unchanged;
- gross MC-EV: unchanged;
- gate/no-gate classification: unchanged;
- first executable trade: unchanged unless another non-MC rule changes it;
- realized P&L and cost accounting: unchanged if the rest of the data pipeline is unchanged.

This is a mathematical consequence of functional identity, not an empirical claim about a different hidden external implementation.

## Predecessor empirical records

The MC1 Phase 2 artifact reports 63 NIFTY and 61 SENSEX executed trades under the locked MC implementation. The separate MC2 Sensex-integrated research reports 97 valid expiries, 52 gated baseline trades, mean net P&L ₹1,727.24 per gated trade and ES99 proxy ₹12,706.60. These are retained as predecessor records, not relabelled as a new MC3 independent rerun.

## Capital interpretation

Because the path transformation is identical, RQ-6 itself cannot create a capital reduction. Any change in capital requirement must come from a change in strike geometry, leg ratios, entry/gating, execution costs, actual margin rules, or data—not from replacing the operational sampler with MC-RQ6-v1.

Actual exchange/SPAN or Paytm Money margin remains a separate measurement problem. ES95/ES99 and stress-loss figures remain proxies unless attributable historical margin records are available.

## Phase 3 acceptance

For the MC1-lineage authority hypothesis, the baseline is method-equivalent. A full raw-data rerun is not required to establish the method-effect delta once exact functional identity has been demonstrated; however, any claim of independent end-to-end numerical reproduction should still be labelled as such and requires the same cached raw data and cost/execution configuration.
