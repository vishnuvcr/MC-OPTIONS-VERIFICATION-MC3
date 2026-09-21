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
