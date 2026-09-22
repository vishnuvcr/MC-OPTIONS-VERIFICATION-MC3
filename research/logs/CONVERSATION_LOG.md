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


## RQ-7 actual capital/margin research — 2026-09-22
User clarified the core objective: reduce total trading capital/margin by changing parameters, while retaining all previous research phases and producing a combined manuscript. A new research was started at Phase 1 in the same repository.

Paytm Money application setup was initiated. Trading API and Live Broadcast were selected. The app-registration form did not save with loopback IP values and gave no explicit error. Decision: do not guess IPs; use a controlled fixed-IP HTTPS callback service for automated authentication. The research remains paper-only and will not place live orders.
## RQ-7 GitHub-only decision — 2026-09-22
User requested a free implementation using GitHub. Decision:
- GitHub Actions runs authenticated read-only Paytm probes.
- GitHub Actions Secrets store credentials/tokens.
- GitHub Pages remains the publication layer.
- No AWS/Lightsail/VPS is required by default.
- The official Paytm SDK manual request-token bootstrap remains user-assisted.
- No live order endpoint is used.
- A manual GitHub workflow and deterministic read-only probe were committed on the RQ-7 Phase 1 branch.
- A paid/fixed-IP callback service will only be introduced if Paytm's current authentication requirements empirically force that dependency.

## RQ-7 TrueIP diagnostic — 2026-09-22
The user provided a TrueIP dashboard screenshot showing the current route is dedicated IPv6 egress with two provisioned IPv6 endpoints. This explains why the Paytm Primary IP field was being tested with IPv6. TrueIP's current public documentation states it also offers dedicated IPv4 for brokers/platforms that require it. Decision: stop retrying the rejected IPv6 value and obtain a stable public IPv4 if available. Security action: the screenshot exposed proxy usernames/egress details, so those credentials should be rotated/revoked and never stored in the repository.
