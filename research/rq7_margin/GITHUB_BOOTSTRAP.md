# RQ-7 GitHub-Only Bootstrap

## 1. Create GitHub Actions secrets

Repository: Settings -> Secrets and variables -> Actions -> New repository secret.

Create:
- PAYTM_MONEY_API_KEY
- PAYTM_MONEY_API_SECRET

If valid session JWTs already exist, also add:
- PAYTM_MONEY_ACCESS_TOKEN
- PAYTM_MONEY_PUBLIC_ACCESS_TOKEN
- PAYTM_MONEY_READ_ACCESS_TOKEN

Never paste these values into ChatGPT, issues, commits or normal workflow inputs.

## 2. Request-token bootstrap

The official Paytm Money Python SDK documents: PMClient(api_secret, api_key), pm.login(state_key), browser authentication, request_token, then pm.generate_session(request_token).

For the GitHub-only architecture, the request token may be placed temporarily in PAYTM_MONEY_REQUEST_TOKEN as a repository secret.

The probe never prints the request token or generated JWTs.

## 3. Run the workflow

Actions -> RQ-7 Phase 1 — Paytm Money GitHub-Only Read-Only Probe -> Run workflow.

The workflow installs the official SDK, performs the authenticated user-details call, reports only a response hash and status, and makes no order request.

## 4. Next phase

After user-details connectivity succeeds, Phase 2 will add read-only probes for security master, NIFTY option chain, SENSEX option chain, live option quote, historical option candle, scrip margin, order margin and charges.

Exact margin request/response schemas will be treated as empirical until validated against the current SDK/API response.

## Important

GitHub-hosted runners do not provide a stable permanent public IP. If Paytm requires a permanently allowlisted callback server for the current application, that constraint will be logged rather than worked around with fabricated IPs.