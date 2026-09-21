# RQ-6 Research Plan — Authoritative BATMAN Monte Carlo Verification

## Core research question

Does the exact authoritative 756-session Monte Carlo path-generation method used by the original BATMAN implementation materially change the estimated baseline economics, terminal-strike selection, capital/risk profile, or the Phase 3–4 conclusions about margin reduction?

## Hypotheses

- H0: Recovering the exact Monte Carlo transformation does not materially change the baseline or the conclusion that no strike-geometry alteration has demonstrated a statistically reliable improvement.
- H1: The exact Monte Carlo transformation materially changes baseline gating, strike selection, risk/capital estimates, or out-of-sample comparisons so that prior conclusions require reclassification or rerun.

## Scientific aims

1. Recover and document the most authoritative available definition of the BATMAN Monte Carlo transformation.
2. Resolve the 756-observation definition and all off-by-one choices.
3. Establish the exact initial-condition and D3 09:30 anchoring convention.
4. Establish the return-sampling dependence structure and random-number convention.
5. Establish terminal-quantile and tradable-strike mapping.
6. Reproduce known original outputs where an auditable original output exists.
7. Quantify the effect of the exact method on baseline economics, risk/capital and the prior strike-search/walk-forward conclusions.
8. Freeze the corrected method as the control model for all subsequent margin-reduction research.

## Phase map

### Phase 0 — Governance and provenance
- Initialize the empty MC3 repository.
- Record predecessor MC1/MC2 provenance.
- Register RQ-6, hypotheses, scope and decision criteria.
- Create status, error and conversation logs.
- Acceptance: repository governance files committed.

### Phase 1 — Authority recovery and method definition
- Search predecessor repositories and all available public sources for the original BATMAN implementation, notebooks, scripts, videos, papers, documentation or reproducible outputs.
- Trace the earliest available MC implementation lineage in MC1.
- Enumerate candidate meanings of “756 sessions”.
- Enumerate candidate path transformations.
- Determine D3 09:30 anchoring rule.
- Determine whether sampling is IID, sequential, without replacement, block-based, bootstrap of returns, or another transformation.
- Determine the RNG/seed convention where evidence exists.
- Determine strike extraction/mapping.
- Build an authority matrix with source, evidence, certainty and unresolved items.
- Acceptance: either an authoritative reconstruction with executable specification, or a documented recovery boundary showing which elements cannot be established from available evidence.

### Phase 2 — Exact implementation and identity tests
- Implement the recovered method without changing locked BATMAN economics.
- Add unit tests for observation definition, sequencing, path construction, anchoring and quantiles.
- Add deterministic method fingerprints for fixed inputs/seed.
- Reproduce any known source output or explain why no exact identity test is possible.
- Acceptance: exact method locked as MC-RQ6-v1 or explicitly marked not-recovered with a reproducible uncertainty set.

### Phase 3 — Baseline revalidation
- Re-run NIFTY and SENSEX with the exact method and common 756-session/5,000-path primary configuration.
- Preserve D3/09:30 rule, four-leg structure, first common executable observation and expiry exit.
- Apply two-point/leg slippage, brokerage, STT, historical lot size and enhanced friction sensitivity.
- Report gate rate, trade count, EV, net P&L, win rate, tail loss, ES95/ES99, drawdown and capital proxies.
- Distinguish actual exchange/broker margin from risk-capital proxies.
- Acceptance: baseline ledger and audit report reproducibly generated.

### Phase 4 — Phase 3–4 revalidation
- Re-run pre-registered strike-geometry candidates under the exact method.
- Freeze candidates using training data only.
- Re-run chronological walk-forward tests.
- Use paired block bootstrap/permutation/sign-flip tests.
- Include Sensex/NIFTY regime diagnostics, execution-cost stress, and selection-effect adjustments.
- Acceptance: direct candidate-vs-baseline comparison and explicit RQ-6 H0/H1 assessment.

### Phase 5 — Integrated manuscript and locked control
- Produce complete manuscript with abstract, research questions, aims, methods, literature, data lineage, results, statistical inference, discussion, strengths, limitations, conclusion, future directions, figures/tables/appendices/supplement.
- Freeze the recovered MC as the new control specification.
- Link the result into MC2's combined research record without overwriting earlier historical results.
- Acceptance: complete reproducible RQ-6 package and explicit downstream-control decision.

## Decision framework

RQ-6 is materially positive when the exact method changes at least one primary quantity enough to alter a pre-registered conclusion. Primary quantities are:
- gross MC-EV;
- gate/no-gate decision;
- selected tradable strikes;
- net P&L;
- win rate;
- tail-loss metrics;
- required capital/margin or declared proxy;
- candidate-vs-baseline effect and inference.

A change is not called material solely because a numeric value moves. The study records both absolute and relative changes and whether any change crosses a decision threshold.

## Statistical plan

- Descriptive distributional comparison of operational versus exact MC outputs.
- Paired expiry-level comparison wherever the same historical observation is available.
- Bootstrap confidence intervals for mean, median and capital metrics.
- Block or cluster bootstrap preserving expiry chronology and market clustering.
- Paired permutation or sign-flip tests for candidate-minus-baseline deltas.
- Win-rate comparison using paired outcome tables where appropriate.
- Strike-displacement and strike-switch rates.
- Gate-decision disagreement rate and paired classification diagnostics.
- Quantile sensitivity analysis around the same MC terminal sample.
- Multiple-testing disclosure for all candidate comparisons.

## Cost and capital convention

Primary execution remains the predecessor locked rule: two option points of adverse slippage per leg, historical lot size, brokerage and STT. Enhanced friction layers are sensitivity analyses.

Capital must be separated into:
1. exchange/SPAN margin if attributable data exist;
2. broker upfront margin if date-specific Paytm Money data exist;
3. premium cashflow required for long legs;
4. transparent research capital/risk proxies such as ES95/ES99 and drawdown when actual margin is unavailable.

No proxy will be relabeled as actual broker margin.

## Data and reproducibility controls

- Cache important source data and dataset revisions rather than downloading on every run.
- Record source URL, revision/hash, retrieval date, schema and checksum.
- Prefer official NSE/BSE data, then attributable broker/reference data, then validated public mirrors.
- No raw-data substitution without a logged decision.
- Every phase gets its own branch and manual workflow_dispatch.
- Every error or limitation is logged before the next phase accepts it.
- Research-plan text changes only when the research design changes; routine progress goes in status logs.

## Known non-repeat rules

The following predecessor errors must not be repeated:
- Do not claim an empty repository contains prior research.
- Do not call a risk proxy actual broker/exchange margin.
- Do not use a temporary canary result as accepted evidence.
- Do not perform post-hoc calibration selection from the same evaluation sample.
- Do not silently change lot-size/cost chronology.
- Do not mix pre-signal and post-signal timestamps.
- Do not infer authoritative MC behavior from wording alone when the source implementation is unavailable.
- Do not use historical results as independent out-of-sample evidence if they were part of model development.
