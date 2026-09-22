# RQ-7 Phase 1 — Authority Matrix

| Capability | Authority | Evidence recovered | Status |
|---|---|---|---|
| Paytm Open API | Paytm Money developer portal | REST APIs provide live market data and account/trading functions | CONFIRMED |
| Historical market data | Paytm Money historical API | 1-minute archived data; contract fields include exchange, expiry, option series/type and strike | CONFIRMED for documented scope; SENSEX option coverage requires live validation |
| Live option data | Official Paytm Money SDK | Live market data API and WebSocket support OPTION scrip type and NSE/BSE exchange type | CONFIRMED |
| Security master | Official Paytm Money SDK/docs | Security master and security IDs are supported | CONFIRMED |
| Position/account state | Paytm Money API | Position details supports NSE/BSE and derivative products | CONFIRMED |
| Order margin | Official Paytm Money SDK | SDK exposes order_margin capability | CONFIRMED as SDK capability; current REST schema requires validation |
| Scrip margin | Official Paytm Money SDK | SDK exposes scrips_margin capability | CONFIRMED as SDK capability; current REST schema requires validation |
| Charges | Official Paytm Money SDK | charges_info capability is exposed | CONFIRMED as SDK capability |
| Historical broker margin | Public docs/SDK | No evidence yet of a historical account-specific margin time series | UNRESOLVED |
| Exchange/SPAN historical margin | Official exchange/clearing sources | Requires separate source audit and acquisition | OPEN |
| Static IP requirement | Paytm app-registration UI | Portal requests primary and secondary IP fields | CONFIRMED operationally; exact allowlisting semantics require validation |
| HTTPS callback | Paytm app-registration UI | Redirect URL should be HTTPS; localhost/127.0.0.1 is allowed for testing | CONFIRMED for app setup; production callback OPEN |
| Live order submission | Paytm Open API | Trading API exposes order APIs | CONFIRMED capability; excluded from RQ-7 |
| Research execution mode | MC3 governance | Paper-only prospective validation is locked | LOCKED |

## Authority URLs

- https://developer.paytmmoney.com/
- https://developer.paytmmoney.com/docs/api/historical-api-beta
- https://github.com/paytmmoney/pyPMClient
- https://github.com/paytmmoney/jsPMClient
- https://developer.paytmmoney.com/docs/api/position-details-api/
- https://developer.paytmmoney.com/docs/api/user-details/

## Phase 1 boundary

The SDK proves that Paytm exposes scrip-margin and order-margin capabilities, but this phase does not claim that those responses constitute historical exchange/SPAN margin or historical account-specific margin. That distinction is a primary design control for Phase 2.
