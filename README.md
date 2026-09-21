# MC3 — BATMAN Monte Carlo Verification / RQ-6

Status: **RQ-6 complete through the planned Phase 5 manuscript/control lock.**

## Research question

Does the exact authoritative 756-session Monte Carlo path-generation method used by the original BATMAN implementation materially change baseline economics, strike selection, capital/risk profile, or the Phase 3–4 conclusions about margin reduction?

## Executive result

The earliest MC1 Monte Carlo implementation has been traced to source commits and reconstructed exactly:

- final 756 finite daily log returns strictly before D3;
- IID sampling with replacement;
- NumPy default_rng(seed=756);
- three future daily-return steps from D3 to expiry;
- D3 09:30 starting spot from the latest pre-09:30 option snapshot, with call-put-parity median within 2% of previous close and previous-close fallback;
- terminal empirical P20/P35/P65/P80 quantiles;
- nearest unique listed-strike mapping with lower-strike tie break.

The deterministic MC-RQ6-v1 control matches the predecessor implementation. Therefore, conditional on the same inputs and non-MC rules, the Monte Carlo method itself does not change terminal paths, strike selection, gross MC-EV, gating, or downstream economics.

An independent external original BATMAN source matching the exact signature was not located in targeted public/GitHub searches, so external-original provenance remains explicitly qualified.

## Phase status

- Phase 0 — DONE
- Phase 1 — DONE (implementation authority established; external-original provenance unresolved)
- Phase 2 — DONE
- Phase 3 — DONE (method-effect identity)
- Phase 4 — DONE (conditional method-stability revalidation)
- Phase 5 — DONE

## Research plan

[Research plan](research/RESEARCH_PLAN.md)

## Phase outputs

[Phase 1 plan](research/phase1/PHASE1_PLAN.md)  
[Method authority matrix](research/phase1/METHOD_AUTHORITY_MATRIX.md)  
[Observation definition](research/phase1/OBSERVATION_DEFINITION.md)  
[Phase 1 results](research/phase1/PHASE1_RESULTS.md)  
[External source audit](research/phase1/EXTERNAL_SOURCE_AUDIT.md)  
[Phase 2 control specification](research/phase2/MC_RQ6_V1_SPEC.md)  
[Identity test protocol](research/phase2/IDENTITY_TEST_PROTOCOL.md)  
[Phase 2 results](research/phase2/PHASE2_RESULTS.md)  
[Phase 3 baseline method effect](research/phase3/BASELINE_METHOD_EFFECT.md)  
[Phase 4 walk-forward method effect](research/phase4/WALKFORWARD_METHOD_EFFECT.md)  
[Complete manuscript](research/manuscript/RQ6_BATMAN_MONTE_CARLO_VERIFICATION_MANUSCRIPT.md)  
[Supplement](research/manuscript/SUPPLEMENT_RQ6.md)  
[Figures and charts](research/manuscript/FIGURES.md)

## Workflows

[Manual workflow index](research/WORKFLOW_INDEX.md)


## Prospective validation — BATMAN PAPER TRADE

The locked MC-RQ6-v1 strategy now has a separate prospective-validation layer:

[Prospective validation hub](research/prospective_validation/README.md)  
[Prospective protocol](research/prospective_validation/PROTOCOL.md)  
[Setup and data-source configuration](research/prospective_validation/SETUP.md)

### Operational workflows

- **BATMAN PAPER TRADE** — scheduled D3 scanning, signal logging, gate-controlled paper entry, append-only records and GitHub Pages publication.
- **BATMAN PAPER TRADE — LIVE MARK** — 10-minute live MTM updates and expiry-day closure.
- **Prospective Validation CI** — syntax and unit-test gate for the module.

Primary records are stored under `data/paper/`. No workflow in this module submits live broker orders.

**SENSEX note:** automatic prospective validation requires an attributable configured BSE/market-data option-chain adapter; the workflow fails closed instead of using synthetic prices.

## Governance logs

[Status log](research/logs/STATUS_LOG.md)  
[Error/limitation log](research/logs/ERROR_LOG.md)  
[Conversation/decision log](research/logs/CONVERSATION_LOG.md)

## Key identity fingerprint

Synthetic fixture terminal-array SHA-256:

6f64abfc0c9d6f9e4e65f52fb47c6f837f208f963cbf05871cb15db8c8626677

## Predecessor findings retained

The inherited MC2 research remains intact. The documented baseline was 97 valid expiries and 52 gross-MC-EV-gated trades, with 76.92% conditional win rate, mean net P&L of ₹1,727.24 per gated trade, and ES99 proxy ₹12,706.60.

The inherited in-sample frontier P22/P33/P67/P78 had an ES99 proxy of ₹12,130.41, about 4.53% below baseline. Chronological walk-forward Split A produced a common-gated delta of -₹161.18 (95% paired bootstrap CI [-₹818.18, +₹334.65], sign-flip p=1.00). Split B produced +₹266.12 (95% CI [-₹914.74, +₹1,270.04], sign-flip p=0.643). These remain predecessor evidence, not new MC3 raw-data reruns.

## Capital/margin rule

ES95/ES99 and stress-loss metrics are risk-capital proxies, not actual Paytm Money or NSE Clearing margin unless separately reconstructed from attributable historical margin data.

The next research question should therefore focus on actual entry and peak capital/margin, with the MC-RQ6-v1 control frozen.

## Branches

- phase-1-rq6-authority-recovery-final
- phase-2-rq6-exact-reconstruction-final
- phase-3-rq6-baseline-revalidation
- phase-4-rq6-walkforward-revalidation
- phase-5-rq6-manuscript-lock\n- prospective-validation-batman-paper-trade
