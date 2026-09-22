# RQ-7 Paytm Money Setup

## Paytm application
- App name: MC OPTIONS
- Product type: Rule Based Trading Platform
- Trading API: enabled
- Live Broadcast: enabled
- Publisher API: not required for this research
- Postback: disabled for the paper-only phase

## GitHub-only architecture
RQ-7 will use GitHub Actions for authenticated read-only API tests and GitHub Pages for publication. No AWS, Lightsail or VPS is required at this stage.

The official Paytm Money Python SDK documents a manual login bootstrap: create a login URL, complete browser authentication, receive a request token, then call generate_session to obtain session JWTs. The one-time browser step remains user-assisted; subsequent read-only API validation runs on GitHub Actions.

See research/rq7_margin/GITHUB_ONLY_ARCHITECTURE.md and research/rq7_margin/GITHUB_BOOTSTRAP.md.

## Secrets
Use GitHub Actions Secrets. Never commit API key, API secret, request token, access token, public access token or read access token.

- PAYTM_MONEY_API_KEY
- PAYTM_MONEY_API_SECRET
- PAYTM_MONEY_REQUEST_TOKEN (temporary bootstrap only)
- PAYTM_MONEY_ACCESS_TOKEN
- PAYTM_MONEY_PUBLIC_ACCESS_TOKEN
- PAYTM_MONEY_READ_ACCESS_TOKEN

## Security guard
RQ-7 must never call live order placement. The GitHub probe contains no order placement, modification or cancellation call.

## Phase 2 read-only tests
1. user details
2. security master lookup
3. NIFTY option chain
4. SENSEX option chain
5. live OPTION quote
6. historical option candle
7. scrip margin
8. order margin for a four-leg BATMAN basket
9. charges information

Raw responses will be cached only after schema validation. Credentials and raw JWT values will never be cached.

## External callback boundary
A fixed public callback server is no longer assumed as the default architecture. If Paytm's current application flow proves that a permanently allowlisted callback is mandatory, that will be recorded as an external dependency. No fabricated loopback or runner IP will be used.