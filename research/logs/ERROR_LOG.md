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


## RQ-7 Phase 1 — Paytm application registration — 2026-09-22
- The Paytm app form accepted the localhost callback format for testing but did not save the application when 127.0.0.1 was entered as both Primary IP and Secondary IP. No explicit validation message was displayed.
- Earlier guidance to duplicate 127.0.0.1 in both IP fields was therefore not accepted as evidence and must not be repeated.
- Resolution: do not invent alternate loopback IPs. Production automation requires a real controlled server with an attributable public IPv4 and HTTPS callback if Paytm's allowlisting requires it.
- This is an external deployment dependency, not a research-method change. The Phase 1 architecture and security boundary are now recorded in research/rq7_margin/SETUP.md.
## RQ-7 Phase 1 — GitHub-only revision — 2026-09-22
- The user explicitly requested a free GitHub-based implementation.
- The architecture was revised so GitHub Actions is the primary authenticated read-only execution environment.
- The paid VPS is removed from the default plan.
- The remaining limitation is Paytm's initial browser authentication/request-token bootstrap and any current requirement for a permanent allowlisted callback. This must be tested rather than assumed.
