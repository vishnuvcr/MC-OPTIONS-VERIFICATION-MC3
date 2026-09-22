# RQ-7 Phase 1 Results — Initial Authority Recovery

Date: 2026-09-22

## Result

Phase 1 established a credible attributable Paytm Money data path for the next phase, but it has not established historical actual margin for every past expiry.

### Confirmed

1. Paytm Money provides a REST Open API for live market data and account/trading functions.
2. The historical API documents archived 1-minute market data and option-contract fields including exchange, expiry, option series/type and strike.
3. The official Paytm Money Python and Node SDKs expose live market data, option-chain functionality, WebSocket streaming, security master, scrip margin, order margin, charges information, and position/account APIs.
4. Official SDK examples support OPTION scrip type and both NSE and BSE exchange types for live WebSocket preferences.
5. MC3 can extend the prospective paper layer with Paytm as an attributable market-data and margin-calculation provider without changing MC-RQ6-v1.

### Not yet established

- Exact current REST request/response schemas for scrip margin and order margin.
- Whether Paytm can return historical margin requirements for arbitrary historical dates.
- Whether account-specific upfront margin can be reconstructed historically from broker records.
- Whether the documented historical endpoint returns the required SENSEX index-option history in practice.
- Exact production authentication callback/IP allowlisting requirements.
- Exact current token lifetime/refresh behavior.

### Decision

Proceed to Phase 2 only after these items are resolved with authenticated, non-secret connectivity tests and raw response fixtures.

## Scientific implication

The question is correctly separated into market-data attribution, which appears feasible, and actual margin attribution, which remains an empirical data-recovery problem. This prevents risk proxies from being relabeled as broker margin.
