# RQ-7 Paytm Money Setup

## Paytm application

- App name: MC OPTIONS
- Product type: Rule Based Trading Platform
- Trading API: enabled
- Live Broadcast: enabled
- Publisher API: not required for this research
- Postback: disabled for the paper-only phase

## Callback architecture

Paytm Money -> authenticated browser login -> HTTPS callback service -> request token -> controlled authentication service -> access/public/read JWTs -> GitHub Actions and cached research data.

The callback service must have a stable public endpoint and, if Paytm enforces IP allowlisting, a fixed public IPv4.

Do not use a mobile IP, home Wi-Fi address as the permanent CI IP, random 127.x.x.x values, or a GitHub Actions runner IP as a permanent allowlist entry.

Paytm's registration page allows localhost/127.0.0.1 callback testing. That is suitable only for local development and is not the production CI architecture.

A small VPS with a fixed public IPv4 and HTTPS is the simplest controlled deployment. The server must be created in the user's own cloud account; this repository cannot safely provision or hold cloud credentials.

## Secrets

Use GitHub Actions Secrets. Never commit API key, API secret/merchant secret, request token, access token, public access token or read access token.

Recommended secret names:

- PAYTM_MONEY_API_KEY
- PAYTM_MONEY_API_SECRET
- PAYTM_MONEY_ACCESS_TOKEN
- PAYTM_MONEY_PUBLIC_ACCESS_TOKEN
- PAYTM_MONEY_READ_ACCESS_TOKEN

Tokens may rotate or expire; Phase 2 will follow the validated Paytm SDK/API flow rather than assuming a permanent JWT.

## Security guard

RQ-7 must never call live order placement. The Trading API is enabled because the same application exposes market/account/margin capabilities. The code must keep a hard paper-only execution guard.

## Phase 2 read-only tests

1. user details;
2. security master lookup;
3. NIFTY option chain;
4. SENSEX option chain;
5. live OPTION quote;
6. historical option candle;
7. scrip margin;
8. order margin for a four-leg BATMAN basket;
9. charges information.

Raw responses will be cached with UTC timestamp, source endpoint, request hash excluding secrets, schema/version, SHA-256 checksum and HTTP status. Credentials and raw JWT values will never be cached.
