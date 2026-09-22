# RQ-6 Status Log

| Step | Phase | Status | Outcome |
|---|---|---|---|
| 0.1 | Foundation | DONE | MC3 initialized as the dedicated RQ-6 repository. |
| 0.2 | Provenance | DONE | MC1/MC2 predecessor repositories identified and audited. |
| 0.3 | Research protocol | DONE | RQ-6 hypotheses, phases, statistical plan and acceptance criteria locked. |
| 1.1 | Authority search | DONE* | MC1 lineage recovered; targeted public searches found no matching independent source. |
| 1.2 | Observation definition | DONE | Control uses the final 756 finite daily log returns before D3; ordinarily 757 closes create them. |
| 1.3 | Path transformation | DONE | IID with-replacement daily-log-return sampling and geometric compounding recovered. |
| 1.4 | D3/09:30 anchoring | DONE | Latest pre-09:30 option snapshot; parity median within 2% of previous close; previous close fallback. |
| 1.5 | Strike mapping | DONE | P20/P35/P65/P80 empirical quantiles mapped to nearest unique listed PE/CE strikes with lower-strike tie break. |
| 1.6 | Identity reproduction | DONE | MC-RQ6-v1 deterministic fixture fingerprint established and tested locally. |
| 2.1 | Exact reconstruction | DONE | MC-RQ6-v1 implemented as traceable control. |
| 2.2 | Identity protocol | DONE | Fixed-input terminal-array SHA-256 identity test added. |
| 3.1 | Baseline method effect | DONE | Functional identity implies zero MC-method effect under identical inputs and non-MC rules. |
| 4.1 | Candidate frontier | DONE (conditional) | Prior frontier remains method-stable conditional on MC1-lineage sampler. |
| 4.2 | Walk-forward | DONE (conditional) | Prior walk-forward conclusions are not altered by MC method replacement; no fresh MC2 raw-data rerun claimed. |
| 5.1 | Manuscript | DONE | Complete RQ-6 manuscript, supplement and figures committed. |
| 5.2 | Control lock | DONE | MC-RQ6-v1 is the traceable control for future margin-reduction research. |
| PV-0 | Prospective design | DONE | Added clean automated paper-trading validation layer; no-live-order rule locked. |
| PV-1 | Implementation | DONE | Core engine, provider adapters, append-only logs, Pages site and manual/scheduled workflows added. |
| PV-2 | Hardening | DONE | Manual diagnostics cannot create prospective trades; D3 capture window, live-mark cadence, cost accounting, lot-size provenance and expiry-day closure were hardened. |
| PV-3 | Validation harness handoff | READY | Branch is ready for review/merge; SENSEX requires a configured attributable live option-chain adapter before live prospective observations are accepted. |

*External-original BATMAN provenance remains unresolved.

| PV-4 | Target-expiry integrity review | DONE | Live strike selection, MC gate pricing, entry quotes and marks are explicitly filtered to the intended contract expiry. |
| PV-5 | Merge | DONE | Prospective validation workflows and Pages publisher were merged into main; no live-order endpoint is included. |
| PV-6 | Data-provider audit | DONE | NIFTY public NSE adapter documented; SENSEX provider boundary and fail-closed rule documented; broker-market-data credentials remain optional. |
| PV-7 | Schedule lock | DONE | D3 scan schedule narrowed to 09:30–09:40 IST capture runs; live marks use the configured instrument close. |
| PV-8 | Instrument-specific marking | DONE | SENSEX marks stop at its derivatives-session boundary; NIFTY marks continue through the NSE derivatives close. |
| PV-9 | CI hardening | DONE | A dedicated BATMAN Prospective Smoke workflow gates executable validation; operational paper runs are not blocked by the separate pytest suite. |
| PV-10 | Operational test isolation | DONE | Scheduled/manual paper-trade runs persist signals/events independently of the historical pytest suite; compile and smoke workflows are separate. |
| PV-11 | Smoke-gate simplification | DONE | Remote smoke gate reduced to deterministic deployment checks; detailed regression scripts remain in the repository but do not block operational signal persistence. Run 35700840566 passed all deployment smoke checks. |
| PV-12 | D3 cron correction | DONE | Corrected GitHub Actions cron from 04:30–04:40 UTC to 04:00–04:10 UTC, matching 09:30–09:40 IST. Run 35701905449 is validating the corrected revision. |

| RQ7-1.1 | RQ-7 Phase 1 | DONE | Paytm Money official portal and official SDK authority recovered; live option streaming, historical market data, scrip/order margin and charges capabilities identified. |
| RQ7-1.2 | RQ-7 Phase 1 | DONE WITH OPEN ITEMS | Historical actual broker margin and exact current margin endpoint schemas remain to be validated with authenticated fixtures. |
| RQ7-1.3 | RQ-7 Phase 1 | BLOCKED FOR AUTOMATED DEPLOYMENT | Paytm app registration did not save the loopback IP configuration; production requires an attributable fixed public IP/callback service rather than invented 127.x.x.x values. |
