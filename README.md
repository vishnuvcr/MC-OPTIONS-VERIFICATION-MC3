# MC3 — BATMAN Monte Carlo Verification / RQ-6

Status: Phase 0 complete; Phase 1 authority recovery in progress

This repository is the separate research track requested for RQ-6: determine whether the exact authoritative 756-session Monte Carlo path-generation method used by the original BATMAN implementation materially changes the locked baseline and therefore the prior Phase 2–4 conclusions.

## Research boundary

RQ-6 is a verification study, not a new strike-optimization search. No new BATMAN parameter search is authorised until the Monte Carlo path transformation is established.

The linked predecessor research remains unchanged:
- MC1: https://github.com/vishnuvcr/MC-OPTIONS-INDEPENDENT-BACKTEST-MC1
- MC2: https://github.com/vishnuvcr/MC-OPTIONS-MARGIN-REDUCTION-MC2

The present repository was initially empty on 2026-09-22. That state is recorded in the error log rather than inferred away.

## Locked questions

1. What exactly are the 756 historical observations?
2. Are they 756 returns, 756 closes, or another transformed sample?
3. How are historical observations sampled, sequenced and compounded?
4. Is each horizon step independent, sequential without replacement, block-based, or otherwise dependent?
5. How is the initial spot anchored at D3 09:30 IST?
6. How are terminal quantiles converted into the four tradable strikes?
7. Can any known original strike/trade output be reproduced exactly?
8. Does an exact reconstruction materially change Phases 2–4?

## Current audit finding

The predecessor MC1 implementation currently performs IID sampling of daily log returns from the last 756 finite observations, seeded with NumPy default_rng(756), and compounds the sampled log returns from an input starting spot. That is an operational reconstruction, not yet established as the authoritative original BATMAN transformation.

The predecessor MC1 locked rule is D3, 09:30 IST, 756-session MC, 5,000 paths, gross MC-EV > 0, P20/P35/P65/P80 terminal quantiles, nearest unique listed strikes, +1/-2/+1/-2 legs, first executable observation after 09:30, expiry exit, two option-points adverse slippage per leg, historical lot size and brokerage/STT.

## Phase status

- Phase 0 — DONE
- Phase 1 — IN PROGRESS
- Phase 2 — PLANNED
- Phase 3 — PLANNED
- Phase 4 — PLANNED
- Phase 5 — PLANNED

See:
- research/RESEARCH_PLAN.md
- research/phase1/PHASE1_PLAN.md
- research/phase1/OBSERVATION_DEFINITION.md
- research/phase1/METHOD_AUTHORITY_MATRIX.md
- research/phase1/LITERATURE_REVIEW.md
- research/logs/STATUS_LOG.md
- research/logs/ERROR_LOG.md
- research/logs/CONVERSATION_LOG.md

## Scientific rule

No numerical conclusion about margin reduction, strike improvement, or production deployment is accepted from an unverified path-generation method. All historical results from MC1/MC2 remain provisional where the path transformation is unresolved.

## Phase 1 reproducibility

Phase 1 has a manual GitHub Actions workflow at .github/workflows/phase-1-rq6-authority.yml.
