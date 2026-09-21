# Error / Limitation Log — RQ-6 and Prospective Validation

Existing RQ-6 limitations remain unchanged.

## Prospective validation limitations
- GitHub Actions schedules are best-effort rather than tick-accurate; actual observation timestamps are logged.
- NSE public option-chain access can change or be rate-limited. The workflow fails closed and logs the provider error.
- SENSEX option-chain access is deliberately adapter-based because BSE's official market-data services may require registration/authentication; no synthetic fallback is permitted.
- Manual `force_today` runs are diagnostics only and are not counted as valid prospective D3 observations unless the logged date is actually D3.
- The paper-trade layer never submits broker orders.
- Current lot-size defaults are locked for the current 2026 regime (NIFTY 65; SENSEX 20). If exchange contract metadata changes, this module must be versioned and updated before affected contracts are accepted.
