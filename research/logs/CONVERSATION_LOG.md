# Conversation / Decision Log

## Prospective validation request
The requested operational layer is separate from the locked MC-RQ6 research control.

User requirement captured:
- automatic D3 scans for NIFTY and SENSEX;
- log signals even when not traded;
- paper-enter only when the trade gate is on;
- mark P/L repeatedly from live market prices;
- keep detailed logs;
- manual workflow named “BATMAN PAPER TRADE”;
- publish a structured and attractive GitHub Pages dashboard.

Implementation decision:
- keep MC-RQ6-v1 frozen;
- no real order submission;
- append-only JSONL event ledger;
- GitHub Actions every 5 minutes for scan/verification and every 10 minutes for live marks;
- Pages deployed from the generated site;
- fail closed on missing or unauthenticated market data.

## PV implementation hardening
Decisions recorded:
- Keep MC-RQ6-v1 unchanged.
- Use 09:25–09:40 IST only as an operational capture window around the frozen 09:30 target; retain actual timestamps.
- Manual force mode is diagnostics-only and cannot open a prospective paper position.
- Mark open paper trades every 10 minutes.
- Apply entry-cost estimates and expiry STT separately from gross MTM.
- Close at expiry after 15:35 IST using the index settlement close.
\n## Target-expiry integrity correction\nThe live chain can contain multiple expiries. All signal and mark calculations are now restricted to the selected contract expiry to prevent cross-expiry quote contamination.\n
## Schedule refinement
D3 scan automation is now limited to three scheduled observations around the 09:30 IST target. Live marks run every 10 minutes through the 15:40 IST derivatives session close, based on current exchange timing references.

## Instrument-specific live marking
SENSEX and NIFTY use separate derivatives-session close boundaries. Post-close manual/scheduled attempts are logged as MARK_SKIP rather than using stale prices.\n
## Final operational handoff correction
A UTC/IST conversion error in the D3 GitHub Actions cron was found during final validation and corrected to 04:00/04:05/04:10 UTC, corresponding to 09:30/09:35/09:40 IST. The successful deployment smoke run 35700840566 verified the current package/import/dashboard/MC/D3 stack before this schedule-only correction.


## PV-13 — user-approved unofficial SENSEX data
User decision: proceed with unofficial SENSEX data so the prospective validation can retrieve SENSEX option-chain data online without a daily manual download.

Implementation: default to the public third-party indiaopt BSEClient path for SENSEX scrip 999920; keep an explicitly configured normalized BSE feed as a higher-priority override; preserve no-live-order and fail-closed rules; record provider provenance in every accepted snapshot.


## PV-14 — rectify live provider failures
User reported the Pages dashboard showing NIFTY HTTP 404 and SENSEX invalid JSON. Investigation identified the NIFTY legacy endpoint as retired; SENSEX indiaopt was reaching BSE but receiving non-JSON content. Rectification branch replaces NIFTY with current indiaopt NSE retrieval and adds bse-options as a second unofficial SENSEX provider. No synthetic data or live orders are permitted.


## PV-14 — rectify live provider failures
User reported the Pages dashboard showing NIFTY HTTP 404 and SENSEX invalid JSON. Investigation identified the NIFTY legacy endpoint as retired; SENSEX indiaopt was reaching BSE but receiving non-JSON content. Rectification branch replaces NIFTY with current indiaopt NSE retrieval and adds bse-options as a second unofficial SENSEX provider. No synthetic data or live orders are permitted.


## PV-15 — user-reported live dashboard regression
The user supplied the post-PV-14 Pages error screen showing a new SENSEX NameError and NIFTY indiaopt normalization failure. This establishes that the prior smoke test verified imports/deployment structure but did not exercise the actual provider result shape. Decision: treat this as a new provider-runtime phase, fix the adapter and add object-result regression tests before accepting a prospective observation.
