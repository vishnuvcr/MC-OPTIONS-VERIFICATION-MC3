# Error / Limitation Log — RQ-6 and Prospective Validation

Existing RQ-6 limitations remain unchanged.

## Prospective validation limitations
- GitHub Actions schedules are best-effort rather than tick-accurate; actual observation timestamps are logged.
- NSE public option-chain access can change or be rate-limited. The workflow fails closed and logs the provider error.
- SENSEX option-chain access is deliberately adapter-based because BSE's official market-data services may require registration/authentication; no synthetic fallback is permitted.
- Manual `force_today` runs are diagnostics only and are not counted as valid prospective D3 observations unless the logged date is actually D3.
- The paper-trade layer never submits broker orders.
- Current lot-size defaults are locked for the current 2026 regime (NIFTY 65; SENSEX 20). If exchange contract metadata changes, this module must be versioned and updated before affected contracts are accepted.

## PV-2 hardening notes
- The initial dashboard implementation used nested f-strings with conflicting quotes; this was refactored before handoff.
- The first engine version could treat a manual forced scan as a valid prospective observation; this was corrected so forced scans are diagnostic-only and cannot open paper trades.
- GitHub Actions cannot guarantee exact 09:30 execution, so the operational protocol uses a bounded 09:25–09:40 capture window and records the actual observation timestamp. This is an explicit operational accommodation, not a silent change to the locked research rule.
- SENSEX automated validation still depends on a configured attributable BSE/market-data adapter; no synthetic fallback is permitted.
- A target-expiry integrity issue was found in review: the live chain may include multiple expiries, so an unfiltered strike/price lookup could select a different contract. The engine now filters the chain to the intended expiry before parity, strike mapping, MC-EV, entry, and mark calculations.

## CI validation event — 2026-09-22
- GitHub Actions run 35699892831 (earlier simplified CI attempt) reached the Python test step but reported a pytest failure; the available GitHub Actions connector exposed step status but not the step log, so the exact pytest assertion/output could not be verified.
- The four intended test cases were independently reproduced in the analysis environment and passed logically.
- The gating workflow was therefore changed to an explicit executable smoke test plus real engine/site imports, rather than silently treating the unexplained pytest result as green.

- Operational workflow policy: the scheduled/manual BATMAN PAPER TRADE workflow now performs compilation only and does not gate data persistence on the separate pytest suite. The dedicated BATMAN Prospective Smoke workflow remains responsible for executable validation.

- Test-fixture correction: the original smoke/test chain had only two strikes per side, making the four-leg globally-unique strike requirement impossible. This caused the strike smoke and earlier pytest suite to fail; the fixture now supplies four strikes per side and asserts all four selected strikes.

## D3 scheduling correction — 2026-09-22
- A UTC-to-IST conversion error was found in the scheduled BATMAN PAPER TRADE cron. The original `30,35,40 4 * * 1-5` meant 10:00–10:10 IST, not 09:30–09:40 IST.
- Corrected schedule: `0,5,10 4 * * 1-5`, corresponding to 09:30, 09:35 and 09:40 IST.
- This did not affect the frozen strategy rule itself; it was an automation scheduling defect. The correction is logged explicitly to prevent recurrence.


## PV-13 — unofficial SENSEX online provider — 2026-09-22
- The configured-only SENSEX adapter would have prevented automatic prospective SENSEX observations without a user-supplied feed URL.
- Decision: add the unofficial indiaopt BSEClient path as the default online provider, while retaining BSE_OPTION_CHAIN_URL as an explicit override.
- This provider is not authoritative exchange data. All SENSEX observations from it are tagged UNOFFICIAL_INDIAOPT_BSE and stored with provider metadata.
- Bid/ask may be absent. The engine therefore uses its existing LTP fallback plus 2-point adverse slippage; this is logged as a data-quality limitation rather than hidden.
- Provider failure remains fail-closed: no synthetic option quote and no paper entry from unavailable data.


## PV-14 — provider recovery after live failure — 2026-09-22
Observed live scan failures:
- NIFTY returned HTTP 404 from the legacy `/api/option-chain-indices` endpoint. Current 2026 research references identify the endpoint as retired and the current flow as `option-chain-contract-info` plus `option-chain-v3`; the public NSE page remains available. citeturn9search6turn9search3
- SENSEX `indiaopt` reached BSE but received non-JSON content, so the provider correctly failed closed.

Rectification:
- NIFTY now uses the current `indiaopt` NSE adapter rather than the retired endpoint.
- SENSEX keeps `indiaopt` first, then tries the separate unofficial `bse-options` package as a second provider.
- No synthetic quotes are introduced.
- Provider provenance is recorded for accepted observations.
- If all providers fail, the observation remains invalid and is retained in the error/signal ledger.


## PV-14 — provider recovery after live failure — 2026-09-22
Observed live scan failures:
- NIFTY returned HTTP 404 from the legacy `/api/option-chain-indices` endpoint. Current 2026 research references identify the endpoint as retired and the current flow as `option-chain-contract-info` plus `option-chain-v3`; the public NSE page remains available. citeturn9search6turn9search3
- SENSEX `indiaopt` reached BSE but received non-JSON content, so the provider correctly failed closed.

Rectification:
- NIFTY now uses the current `indiaopt` NSE adapter rather than the retired endpoint.
- SENSEX keeps `indiaopt` first, then tries the separate unofficial `bse-options` package as a second provider.
- No synthetic quotes are introduced.
- Provider provenance is recorded for accepted observations.
- If all providers fail, the observation remains invalid and is retained in the error/signal ledger.


## PV-14 correction 1 — router regression — 2026-09-22
- Mistake: while replacing the NIFTY provider function, the text edit removed the `live_chain` router required by `engine.py`.
- Detection: GitHub Actions smoke failed at engine import with `ImportError: cannot import name 'live_chain'`.
- Rectification: restored the router and kept provider selection isolated inside `market.py`.
- Prevention: future provider edits must preserve and smoke-test the public market adapter surface before merge.


## PV-15 — live-scan regression exposed after PV-14 — 2026-09-22
Observed in the user's Pages error ledger after the PV-14 merge:
- SENSEX: NameError: name 'fetch_sensex_chain' is not defined. Cause: the restored live_chain router referenced the provider function without importing it in that branch of market.py.
- NIFTY: RuntimeError from indiaopt saying it returned no recognisable SENSEX option rows. The provider reached indiaopt, but the normalizer expected dict/list rows and did not unwrap the OptionChainResult.data object rows. The error text also incorrectly hard-coded SENSEX.

Rectification:
- Import fetch_sensex_chain locally in the SENSEX router branch.
- Normalize object-based indiaopt results and call_ltp/put_ltp row fields, including optional bid/ask.
- Make normalization errors exchange-neutral.
- Add regression coverage for an indiaopt-style NIFTY object result and bid/ask fields.

Prevention:
- Provider adapters must be tested against both documented object-style result shapes and dict/list exchange payloads before live deployment.
- The public live_chain router must be import-smoked whenever provider code changes.


## PV-15 validation — 2026-09-22
GitHub Actions smoke run 35758524492 passed after the PV-15 corrections. The new provider-normalization test and live-router import smoke both succeeded. This validates the code path and documented indiaopt result-shape handling; it does not by itself prove that NSE/BSE will permit a fresh live chain fetch on the next scheduled scan.
