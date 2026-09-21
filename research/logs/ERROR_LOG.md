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
