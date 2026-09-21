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