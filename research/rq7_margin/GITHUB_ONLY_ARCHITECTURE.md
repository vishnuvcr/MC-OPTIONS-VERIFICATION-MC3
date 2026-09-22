# RQ-7 GitHub-Only Architecture

Date: 2026-09-22

## Decision

RQ-7 will use GitHub as the primary execution, storage, CI and publication platform. No AWS, Lightsail, VPS or paid callback server is required for the research workflow.

GitHub Actions can run authenticated Paytm Money read-only tests once required credentials/tokens are stored as GitHub Actions Secrets. GitHub Pages remains the publication layer.

## Authentication boundary

The official Paytm Money Python SDK documents a manual login flow: create a login URL, complete username/password/OTP/passcode in a browser, receive a request_token, and then call generate_session to obtain access/public/read JWTs. Therefore the first authentication step cannot be made fully unattended by a normal GitHub-hosted runner.

One-time bootstrap:
1. Generate the Paytm login URL using the official SDK.
2. Complete Paytm authentication in the browser.
3. Obtain the resulting request_token.
4. Store it temporarily as the GitHub Actions secret PAYTM_MONEY_REQUEST_TOKEN.
5. Run the manual RQ-7 GitHub workflow.
6. The workflow exchanges the request token for session tokens in memory.
7. The workflow performs only read-only validation.
8. Do not print or commit any token.
9. Remove temporary request-token material after successful bootstrap and retain only the minimum credentials supported by the validated Paytm flow.

## Security

No workflow may place, modify or cancel a live order. GitHub Actions Secrets are the only approved repository-side secret store. No Paytm secret, JWT, request token, access token or API secret may enter Git.

## GitHub components

- .github/workflows/rq7-phase1-paytm-github.yml — manual authenticated read-only validation.
- src/rq7_margin/paytm_github_probe.py — deterministic, paper-only connectivity probe.
- research/rq7_margin/GITHUB_BOOTSTRAP.md — secret and bootstrap procedure.

## Acceptance criterion

RQ-7 remains Phase 1 until the GitHub workflow produces sanitized, attributable, authenticated response fixtures for read-only capabilities and the exact margin response schemas are documented.

## Cost

Expected infrastructure cost: ₹0 for GitHub-hosted Actions/Pages under the applicable GitHub plan and usage limits. No paid VPS is part of the research design.