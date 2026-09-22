# RQ-7 Phase 1 Results — Initial Authority Recovery

Date: 2026-09-22

## Result
Phase 1 established a credible attributable Paytm Money data path and a GitHub-only execution design for the next phase, but it has not established historical actual margin for every past expiry.

## Confirmed
1. Paytm Money provides a REST Open API for live market data and account/trading functions.
2. The historical API documents archived 1-minute market data and option-contract fields including exchange, expiry, option series/type and strike.
3. The official Paytm Money Python and Node SDKs expose live market data, option-chain functionality, WebSocket streaming, security master, scrip margin, order margin, charges information, and position/account APIs.
4. Official SDK examples support OPTION scrip type and both NSE and BSE exchange types for live WebSocket preferences.
5. The official Python SDK documents manual login, request token and generate_session.
6. GitHub Actions Secrets provide an appropriate repository-side store for Paytm credentials/tokens, and GitHub Actions provides the execution environment for read-only validation.
7. A dedicated GitHub-only RQ-7 workflow and paper-only probe have been added.

## Not yet established
- Exact current REST request/response schemas for scrip margin and order margin.
- Whether Paytm can return historical margin requirements for arbitrary historical dates.
- Whether account-specific upfront margin can be reconstructed historically from broker records.
- Whether the documented historical endpoint returns the required SENSEX index-option history in practice.
- Exact current token lifetime/refresh behavior.
- Whether the current Paytm application requires a permanent public callback/IP for unattended authentication.

## Decision
Proceed to Phase 2 using the GitHub-only architecture. First gate: authenticated non-secret user-details response from GitHub Actions. Then expand to option-chain, historical-data, margin and charges probes.

## Scientific implication
Market-data attribution appears feasible, while actual margin attribution remains an empirical data-recovery problem. Risk proxies must not be relabeled as broker margin.

No margin-reduction claim is made at Phase 1.

## 2026-09-22 — Zero IP broker allowlist check

The user-provided Zero IP broker-API catalogue was inspected. The visible supported broker list includes 5Paisa, Alice Blue, Dhan, Flattrade, Fyers, Groww, ICICIDirect, IIFL Securities, Kotak Securities (Neo), Upstox and Zerodha Kite; Paytm Money is not shown in the visible catalogue. Zero IP describes domain-locked egress, so the current evidence does not establish that a Zero IP tunnel can reach Paytm Money. Paytm Money's official API remains independently confirmed, including REST APIs and Python SDK support. Decision: do not enter the Zero IP address in Paytm's Primary IP field yet. Either verify that Zero IP can explicitly add Paytm Money API domains, obtain written support confirmation, or use a different stable-IP route.


## 2026-09-22 — Stable/true egress IP obtained

User reports that a true/stable egress IP has now been obtained. This removes the immediate uncertainty around the availability of a fixed source IP, but Paytm allowlisting and end-to-end API connectivity remain to be empirically verified. The IP value itself is not recorded in the repository or chat. Next validation: configure the Paytm Money app Primary IP with the obtained stable egress IP, keep Secondary IP blank unless a second stable IP is intentionally provisioned, then perform the GitHub/Python read-only connectivity test. Zero IP is not assumed to be the provider unless independently confirmed.
