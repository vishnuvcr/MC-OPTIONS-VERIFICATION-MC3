# RQ-6 BATMAN Monte Carlo Verification Manuscript

## Does the Exact 756-Session Monte Carlo Path-Generation Method Change the Baseline, Strike Selection, Capital/Risk Profile, or Prior Margin-Reduction Conclusions?

**Project:** MC-OPTIONS-VERIFICATION-MC3  
**Research question:** RQ-6  
**Date:** 2026-09-22  
**Status:** Completed through the planned Phase 5 manuscript lock, with external-original-source provenance qualified as unresolved.

---

## Abstract

### Background

The earlier BATMAN research used a 756-session Monte Carlo reconstruction to generate terminal distributions, select four tradable strikes and gate trades before expiry. The downstream margin-reduction research concluded that tested strike-geometry changes had not produced statistically reliable improvement and that observed capital reductions were proxy-based rather than demonstrated reductions in actual NSE Clearing or Paytm Money margin. That conclusion was explicitly provisional because the exact original BATMAN Monte Carlo transformation had not been established as authoritative.

### Objective

RQ-6 asked whether recovering the exact Monte Carlo path-generation method materially changes the baseline economics, selected strikes, capital/risk profile, or the Phase 3–4 candidate-frontier and walk-forward conclusions.

### Methods

The study used a finite five-phase protocol. First, the earliest MC1 implementation lineage was traced. The earliest Monte Carlo module was found in commit 20b606a015a54b08f77e088faf74aae7df7ed5cf. The reconstructed method filters daily observations strictly before D3, computes close-to-close log returns, retains the final 756 finite returns, samples each future step independently with replacement using NumPy default_rng(seed=756), and compounds the sampled log returns from a D3 09:30-derived starting spot. The horizon is three daily steps from D3 to expiry. Terminal empirical quantiles at 20%, 35%, 65% and 80% are mapped to nearest unique listed strikes, with option-side restrictions and a deterministic lower-strike tie break.

A deterministic identity fixture was added. For a fixed synthetic 900-return input, S0=100, three-step horizon, 100 paths and seed 756, the terminal-array SHA-256 fingerprint is 6f64abfc0c9d6f9e4e65f52fb47c6f837f208f963cbf05871cb15db8c8626677.

### Results

The earliest MC1 implementation is exactly reproducible from source. Its functional behavior is therefore identical to the RQ-6 control specification. Under identical inputs, replacing the prior operational reconstruction label with MC-RQ6-v1 produces zero mathematical difference in terminal paths, terminal quantiles, strike targets, strike selection, gross MC-EV, gate classification, and any deterministic downstream calculation.

The remaining provenance question is whether the earliest MC1 implementation was itself the original external BATMAN implementation. Targeted public GitHub and code searches did not identify another source matching the exact combination of a 756-history Monte Carlo, D3 09:30 anchor, P20/P35/P65/P80 terminal quantiles and the locked four-leg structure. Generic public Batman trading descriptions are heterogeneous and do not establish this method.

The inherited MC2 empirical results therefore remain conditionally method-stable for the MC1-lineage sampler, but MC3 does not claim a fresh independent re-run of the MC2 raw option dataset because that cache is not present in MC3.

### Conclusion

For the traceable MC1 implementation, RQ-6 does not uncover a hidden Monte Carlo transformation that would change the prior results. The corrected control can be locked as MC-RQ6-v1. Consequently, further margin-reduction work should proceed from this locked control and concentrate on actual capital/margin measurement, not on re-opening the Monte Carlo sampler without new provenance evidence. The external-original-authority limitation remains explicitly documented.

---

## 1. Research question and hypotheses

### Primary research question

Does the exact authoritative 756-session Monte Carlo path-generation method used by the original BATMAN implementation materially change the estimated baseline economics, strike selection, capital/risk profile, and the Phase 3–4 conclusions about margin reduction?

### Null hypothesis

Recovering the exact Monte Carlo transformation does not materially change the baseline or the conclusion that no tested strike-geometry alteration has demonstrated statistically reliable improvement.

### Alternative hypothesis

The exact Monte Carlo transformation materially changes baseline gating, strike selection, risk/capital estimates, or out-of-sample comparisons, making previous conclusions unreliable.

### Operational definition of materiality

A change is material only when it is large enough to change a pre-registered research decision. The primary decision quantities are:

1. gross MC-EV;
2. gate/no-gate status;
3. terminal quantile targets and tradable strikes;
4. realized net P&L;
5. tail-loss and capital-risk statistics;
6. required capital or a declared capital proxy;
7. candidate-versus-baseline effect and inferential conclusion.

A numerically non-zero difference that does not change any decision is reported as a sensitivity, not as evidence of a changed conclusion.

---

## 2. Aims and objectives

1. Recover the most authoritative traceable Monte Carlo definition available.
2. Resolve whether “756 sessions” means 756 closes, 756 returns, or another transformed sample.
3. Resolve the exact historical-window boundary.
4. Resolve the D3 09:30 starting-spot construction.
5. Resolve the sampling dependence structure and random-number convention.
6. Resolve terminal-quantile and tradable-strike mapping.
7. Create an executable deterministic identity test.
8. Determine whether the repaired MC materially changes downstream research conclusions.
9. Freeze the corrected model as the control for later margin-reduction experiments.
10. Preserve a reproducible record of uncertainty and provenance limitations.

---

## 3. Phase structure and stopping rule

### Phase 0 — Governance and provenance

Created the dedicated MC3 repository, registered RQ-6, defined hypotheses, statistical plan, capital conventions and non-repeat rules.

### Phase 1 — Authority recovery

Audited MC1 history, searched for independent source evidence, resolved the historical-observation boundary, documented the D3 09:30 anchor and built the method-authority matrix.

### Phase 2 — Exact reconstruction

Implemented MC-RQ6-v1, added deterministic unit tests, and created the terminal-array identity fingerprint.

### Phase 3 — Baseline method-effect revalidation

Established the mathematical effect of substituting MC-RQ6-v1 for the MC1-lineage operational implementation.

### Phase 4 — Candidate and walk-forward method-effect revalidation

Mapped the result to the inherited Phase 3–4 strike-frontier and walk-forward conclusions, with explicit qualification that MC3 does not contain the raw MC2 option cache.

### Phase 5 — Manuscript and control lock

Integrated methods, results, limitations and downstream research direction into this manuscript and locked MC-RQ6-v1 as the traceable control.

The stopping rule is reached when the planned five phases are complete. Further work is treated as a new research question, not an extension of RQ-6.

---

## 4. Data and provenance

### 4.1 Predecessor repositories

- MC1: vishnuvcr/MC-OPTIONS-INDEPENDENT-BACKTEST-MC1
- MC2: vishnuvcr/MC-OPTIONS-MARGIN-REDUCTION-MC2

### 4.2 MC1 implementation lineage

The earliest identifiable MC implementation commit was:

20b606a015a54b08f77e088faf74aae7df7ed5cf — Add Monte Carlo and strike selection module.

The earliest strategy implementation is:

43ec07c9a29d1c8429c2542b6dfce0497ee7c2c4 — Add locked strategy model functions.

The first expiry trade engine is:

63ff284d0b5a1ed211ff85845d02c13cc038b024 — Add expiry trade engine.

These commits provide direct evidence of what the predecessor implementation actually executed.

### 4.3 External-source recovery

Targeted searches for the exact implementation signature did not identify another public implementation reproducing all of the following simultaneously:

- 756 historical observations;
- D3 09:30 signal/anchor;
- P20/P35/P65/P80 terminal quantile strike selection;
- the +1 / -2 / +1 / -2 four-leg structure;
- the same Monte Carlo mechanism.

The absence of a public match is negative evidence only. It is not proof that no private, deleted, unpublished or otherwise inaccessible original source exists.

### 4.4 Important distinction

RQ-6 therefore separates:

Implementation authority: the earliest MC1 lineage is directly traceable and exactly reproducible.

External originality authority: an independent original BATMAN source has not been located.

The first claim is established. The second remains unresolved.

---

## 5. Exact Monte Carlo method

### 5.1 Historical observations

For each D3 signal date:

1. include only daily observations with date strictly before D3;
2. compute close-to-close log returns r_t = ln(C_t) - ln(C_(t-1));
3. remove non-finite values;
4. retain the final 756 finite log-return observations.

Therefore, where each return is formed from two adjacent closes, 756 valid log returns normally require 757 close observations.

This resolves the most important off-by-one ambiguity: the MC input is a 756-observation return vector, not a 756-element close vector.

### 5.2 Signal-day boundary

The D3 close itself is excluded from the historical bootstrap sample.

The D3 intraday option snapshot is used for the signal and starting-spot construction, but it is not inserted as a daily-close return observation.

### 5.3 Sampling

For a three-step horizon, each path receives three random historical-return indices i1, i2, i3, with each index uniform on {0,...,755} and sampled with replacement, using one continuous NumPy default_rng(756) stream.

There is no block bootstrap, no without-replacement permutation and no explicit serial-dependence preservation in the MC1-lineage implementation.

### 5.4 Horizon

The strategy expiry-session function identifies:

- D3 signal session;
- D2;
- D1;
- expiry.

The simulation horizon passed to the Monte Carlo engine is 3.

### 5.5 Path transformation

For each path:

S_T = S_0 × exp(r1 + r2 + r3).

The method is therefore an historical-return bootstrap with log-return compounding.

### 5.6 D3 09:30 starting spot

The engine first takes the latest option timestamp at or before 09:30 IST on D3.

The preferred starting spot is constructed by put-call parity:

S_hat(K) = K + CE(K) - PE(K).

Valid same-strike estimates within 2% of the previous close are retained, and the median estimate is used.

If no valid parity estimate exists, the previous close is used as the fallback.

This is more precise than describing the method simply as “start at D3 09:30 spot”.

### 5.7 Terminal quantiles

The simulated terminal spots are converted to:

- 20th percentile → P20;
- 35th percentile → P35;
- 65th percentile → P65;
- 80th percentile → P80.

The predecessor uses NumPy empirical quantiles.

### 5.8 Tradable-strike mapping

Each continuous model target is mapped to an actually listed strike:

1. restrict to PE or CE according to the target leg;
2. choose the nearest available strike;
3. require all four selected strikes to be unique;
4. resolve an exact distance tie to the lower strike.

This is a deterministic mapping from a continuous model distribution to a discrete exchange contract grid.

---

## 6. Locked BATMAN portfolio and execution model

The MC model is downstream of the locked portfolio:

- +1 P35 PE;
- -2 P20 PE;
- +1 P65 CE;
- -2 P80 CE.

The gross MC-EV gate is mean(simulated portfolio payoff) minus entry premium cashflow > 0.

The first executable timestamp after the signal is selected only when all four required option records are simultaneously executable.

The historical transaction model retains:

- two option points of adverse slippage per execution leg;
- brokerage;
- applicable STT;
- historical contract lot size.

Enhanced friction variants remain sensitivity analyses.

Actual exchange/SPAN margin, broker-required upfront margin, premium cash requirements and risk proxies are treated as separate quantities. ES95/ES99 or stress-loss values are not relabelled as actual Paytm Money or exchange margin.

---

## 7. Statistical methodology

### 7.1 Deterministic identity

The highest-priority test is functional identity. For fixed:

- ordered historical-return vector;
- S0;
- horizon;
- path count;
- seed;
- software versions;

the terminal array must match exactly.

A SHA-256 hash of the raw terminal array is used as a compact identity fingerprint.

### 7.2 Paired downstream analysis

Where historical expiry-level observations are available, old and corrected implementations should be compared on the same expiry:

- gate disagreement rate;
- strike-switch rate;
- gross MC-EV difference;
- net P&L difference;
- capital requirement difference;
- tail-risk difference.

### 7.3 Inference

The pre-registered downstream statistical approach includes:

- paired expiry-level bootstrap confidence intervals;
- block or cluster bootstrap preserving chronological clustering;
- paired permutation/sign-flip tests;
- win-rate paired diagnostics;
- multiple-testing disclosure.

The present RQ-6 method-effect result is stronger than a noisy statistical difference test because the reconstructed functions are deterministic-identical to the predecessor implementation under identical inputs.

---

## 8. Results

### 8.1 Sub-question 1 — What exactly are the 756 observations?

Answer: 756 finite daily log returns, calculated only from observations strictly before D3 and retained as the final 756 returns.

This requires 757 close values under ordinary adjacent differencing. The D3 close is excluded.

### 8.2 Sub-question 2 — How are returns sampled and transformed?

Answer: IID sampling with replacement from the 756-return vector, using NumPy default_rng(756). Sampled log returns are summed and exponentiated from S0.

### 8.3 Sub-question 3 — How is initial spot anchored at D3 09:30?

Answer: the latest option observation at or before 09:30 IST is used; the preferred S0 is the median call-put-parity estimate within 2% of the previous close; previous close is a fallback.

### 8.4 Sub-question 4 — Are horizon steps independent?

Answer: yes, at the sampler level they are independent draws with replacement from the historical return vector. There is no explicit block dependence.

### 8.5 Sub-question 5 — How are terminal quantiles converted to four strikes?

Answer: empirical terminal spot quantiles at 0.20, 0.35, 0.65 and 0.80 are mapped to the nearest unique listed PE/CE strikes with deterministic lower-strike tie-breaking.

### 8.6 Sub-question 6 — Does the exact method reproduce original outputs?

The exact predecessor implementation is reproducible, including the deterministic terminal-array fixture:

SHA-256 = 6f64abfc0c9d6f9e4e65f52fb47c6f837f208f963cbf05871cb15db8c8626677.

No independent original BATMAN trade or strike artifact was found that could serve as an external identity target.

### 8.7 Sub-question 7 — Do Phases 2–4 reproduce the same conclusions?

For the MC1-lineage implementation, yes: because MC-RQ6-v1 is functionally identical, any deterministic downstream quantity is invariant when data, costs, execution and non-MC rules are unchanged.

The inherited MC2 Phase 3–4 statistics therefore remain conditionally method-stable, but MC3 does not claim an independent raw-data replication because the MC2 historical option cache is not stored in MC3.

---

## 9. Inherited baseline and candidate-frontier evidence

### 9.1 MC1 raw-option Phase 2 record

The predecessor MC1 candidate artifact reported:

| Metric | NIFTY | SENSEX |
|---|---:|---:|
| Executed trades | 63 | 61 |
| Mean MC-EV, points | 52.146 | 234.738 |
| Mean net P&L, ₹ | 1,183.66 | 2,507.53 |
| Net ES99 proxy, ₹ | -38,992.43 | -38,352.77 |
| Sequential-trade max drawdown, ₹ | -50,343.72 | -66,886.42 |

The artifact was explicitly described as a candidate descriptive backtest, not final inference.

The later MC1 Phase 8 revalidation used the same primary 756-session/5,000-path calibration and reported 63 NIFTY and 61 SENSEX trades with mean net P&L of ₹966.46 and ₹2,508.06 respectively under its final documented friction configuration. These figures are configuration-specific and are retained as predecessor evidence rather than recalculated by MC3.

### 9.2 MC2 integrated baseline

The predecessor MC2 combined conclusion reported:

- 97 valid expiries;
- 52 gross-MC-EV-gated baseline trades;
- 76.92% conditional win rate;
- mean net P&L ₹1,727.24 per gated trade;
- ES99 proxy ₹12,706.60.

### 9.3 In-sample frontier

The prior in-sample frontier point P22/P33/P67/P78 had:

- mean net P&L per eligible expiry: ₹1,016.80;
- mean net P&L per gated trade: ₹1,730.35;
- win rate: 78.95%;
- ES99 proxy: ₹12,130.41;
- ES99 proxy reduction: about 4.53%.

### 9.4 Walk-forward evidence

Split A:

- training selection: P20.5/P35/P65/P79.5;
- 2026 candidate-minus-baseline: -₹161.18;
- 95% paired bootstrap interval: [-₹818.18, +₹334.65];
- sign-flip p=1.00.

Split B:

- training selection: P22/P33/P67/P78;
- 2026 candidate-minus-baseline: +₹266.12;
- 95% paired bootstrap interval: [-₹914.74, +₹1,270.04];
- sign-flip p=0.643.

Because the intervals cross zero and the paired tests are not significant, the predecessor research did not establish a statistically reliable production improvement.

RQ-6 does not change that conclusion for the MC1-lineage sampler.

---

## 10. Capital and margin interpretation

The central margin-reduction objective is to reduce the actual amount of capital that must be available or blocked, not merely a statistical tail-loss proxy.

RQ-6 does not itself produce a capital reduction because it recovers the same MC transformation used by the traceable predecessor implementation.

Any genuine capital reduction must therefore arise from one or more of:

- strike geometry;
- leg ratios;
- gating/entry thresholds;
- actual exchange margin offsets;
- broker-specific margin rules;
- execution/premium structure;
- contract selection;
- holding-period overlap.

The earlier MC2 capital track found only proxy-based changes because complete date-specific historical SPAN and Paytm Money margin data were unavailable in the working cache. That limitation remains.

---

## 11. Discussion

### 11.1 What RQ-6 resolved

The largest methodological ambiguity — what “756-session Monte Carlo” actually means — has now been resolved for the predecessor implementation.

It is not a 756-close simulation. It is a 756-return simulation.

It is not a contiguous block bootstrap. It is an IID historical-return bootstrap.

It is not anchored blindly at a raw 09:30 index tick. The starting spot is derived from the latest pre-09:30 option snapshot using call-put parity, with previous close fallback.

It is not a one- or two-day expiry model. The locked engine uses three simulated daily-return steps from D3 through expiry.

These details are sufficiently specific to make the predecessor implementation independently reproducible.

### 11.2 What RQ-6 did not resolve

RQ-6 did not discover an independent public source proving that the MC1 code is the original external BATMAN implementation.

This is an authorship/provenance limitation, not an implementation ambiguity.

The scientific response is to retain the distinction rather than manufacture certainty.

### 11.3 Why generic “Batman” sources were not accepted as authority

Public trading discussions and strategy pages use the word “Batman” for multiple incompatible option structures. Some use symmetric or ratio butterflies; others use delta-based or premium-based leg selection. None located in the targeted search matched the exact RQ-6 signature.

Accordingly, generic Batman descriptions were not allowed to overwrite the repository's direct source-code evidence.

### 11.4 Implications for margin-reduction research

The prior margin-reduction work should not restart the Monte Carlo method from scratch. MC-RQ6-v1 is now a locked control.

Future experiments should change only the pre-registered parameter families of interest and keep MC-RQ6-v1 fixed unless a new, higher-authority external source is found.

This sharply reduces the risk of optimizing the optimizer or comparing candidates against an unstable control.

---

## 12. Strengths

1. Direct lineage evidence: the earliest MC1 Monte Carlo commit was identified and audited.
2. Exact deterministic reconstruction: the sampling, horizon and transformation are executable rather than inferred from prose.
3. Explicit off-by-one resolution: 756 returns versus 756 closes is no longer ambiguous for the control model.
4. Information-set integrity: the D3 09:30 anchor is separated from the historical return sample.
5. Reproducible identity fingerprint: fixed-input terminal arrays can be checked byte-for-byte.
6. Provenance discipline: implementation authority and external-original authority are reported separately.
7. No post-hoc tuning: RQ-6 does not reopen strike optimization.
8. Capital realism: actual margin and research proxies remain explicitly separated.
9. Chronological inference framework: inherited walk-forward results are preserved with their confidence intervals and permutation tests.
10. Audit trail: status, errors and user-visible research decisions are retained in the repository.

---

## 13. Limitations

1. The original external BATMAN source was not located.
2. MC3 does not currently contain the full MC2 raw option cache, so the downstream conclusion is conditional method-equivalence rather than a new independent end-to-end rerun.
3. Historical actual broker margin and exchange SPAN files are not part of this RQ-6 cache.
4. The deterministic hash establishes software identity for a controlled fixture, not historical-data identity.
5. The MC1-lineage RNG is a NumPy implementation detail; if the external BATMAN source used another RNG implementation with the same seed semantics, the generated path realization could differ even under the same conceptual algorithm.
6. Public source searches cannot prove non-existence of private or inaccessible original code.
7. Predecessor empirical results inherit their documented option-data coverage and costs; RQ-6 does not erase those source limitations.

---

## 14. Conclusion

RQ-6 establishes that the predecessor MC1 Monte Carlo method can be reconstructed exactly and frozen as MC-RQ6-v1:

- 756 finite daily log returns before D3;
- IID sampling with replacement;
- NumPy default_rng seed 756;
- three daily steps to expiry;
- D3 09:30 option-parity-derived starting spot with previous-close fallback;
- terminal quantiles P20/P35/P65/P80;
- nearest unique listed strikes;
- locked +1/-2/+1/-2 BATMAN geometry.

For that traceable implementation, the exact reconstructed method does not materially alter baseline economics, strike selection or Phase 3–4 conclusions because it is functionally identical to the earlier implementation.

The remaining uncertainty is external provenance: an independent original BATMAN implementation matching these details has not been located.

Therefore the scientifically appropriate downstream action is to lock MC-RQ6-v1 as the control and proceed to actual capital/margin optimization using independently reconstructed historical margin requirements, while retaining all previous MC2 results and their limitations.

---

## 15. Future research

The next research should be a new, separately versioned question focused on actual total trading capital:

1. reconstruct date-specific NSE Clearing/SPAN risk parameters for NIFTY and SENSEX;
2. reconstruct Paytm Money upfront margin requirements where attributable historical records are available;
3. calculate entry and peak capital for the locked one-lot baseline;
4. rerun pre-registered strike-location and leg-ratio families under the frozen MC-RQ6-v1 control;
5. optimize actual capital requirement subject to pre-registered net-P&L, win-rate, drawdown and tail-risk constraints;
6. perform chronological walk-forward validation and transaction-cost stress;
7. retain NIFTY/SENSEX and regime diagnostics as cross-market validation layers.

A successful future result should report rupees of actual capital saved, percentage capital saved, effect on net expectancy and risk, and whether the saving survives out-of-sample validation.

---

# Appendix A — Reproducible pseudocode

    for each expiry:
        identify D3
        daily_hist = daily_rows where date < D3
        logret = diff(log(daily_hist.close))
        hist = last 756 finite logret values

        snapshot = latest option timestamp <= 09:30 IST
        fallback = previous daily close

        parity_spots = K + CE(K) - PE(K)
        S0 = median(parity_spots within 2% of fallback)
        if unavailable:
            S0 = fallback

        terminals = []
        for path in 1..5000:
            draw 3 historical returns independently with replacement
            ST = S0 * exp(sum(draws))
            terminals.append(ST)

        q20, q35, q65, q80 = empirical_quantiles(terminals)

        P20 = nearest unique listed PE strike to q20
        P35 = nearest unique listed PE strike to q35
        P65 = nearest unique listed CE strike to q65
        P80 = nearest unique listed CE strike to q80

        evaluate gross MC-EV
        if gross MC-EV <= 0:
            reject trade
        else:
            execute first common executable timestamp after 09:30

# Appendix B — Identity fixture

Input:
- historical returns: 900 values formed by repeating [0.01, -0.005, 0.002];
- S0 = 100;
- horizon = 3;
- paths = 100;
- seed = 756.

Expected terminal-array SHA-256:

6f64abfc0c9d6f9e4e65f52fb47c6f837f208f963cbf05871cb8c8626677

# Appendix C — Method-authority matrix summary

| Component | Status |
|---|---|
| 756-return observation count | Exact in MC1 lineage |
| Historical boundary | Exact in MC1 lineage |
| IID with replacement | Exact in MC1 lineage |
| Three-step horizon | Exact in MC1 lineage |
| NumPy seed 756 | Exact in MC1 lineage |
| D3 09:30 parity anchor | Exact in MC1 lineage |
| Quantiles | Exact in MC1 lineage |
| Strike mapping | Exact in MC1 lineage |
| External original BATMAN provenance | Unresolved |

# Appendix D — Data and cost controls

All downstream numerical claims must retain:

- dataset revision/hash;
- retrieval date;
- underlying instrument;
- expiry-date convention;
- option timestamp convention;
- lot-size schedule;
- two-point/leg slippage;
- brokerage;
- STT;
- any enhanced friction layer;
- distinction between actual margin and risk proxies.

# Appendix E — Reproducibility and research-governance links

See repository files:

- research/RESEARCH_PLAN.md
- research/phase1/PHASE1_PLAN.md
- research/phase1/METHOD_AUTHORITY_MATRIX.md
- research/phase1/OBSERVATION_DEFINITION.md
- research/phase2/MC_RQ6_V1_SPEC.md
- research/phase2/IDENTITY_TEST_PROTOCOL.md
- research/phase2/PHASE2_RESULTS.md
- research/phase3/BASELINE_METHOD_EFFECT.md
- research/phase4/WALKFORWARD_METHOD_EFFECT.md
- research/logs/STATUS_LOG.md
- research/logs/ERROR_LOG.md
- research/logs/CONVERSATION_LOG.md
