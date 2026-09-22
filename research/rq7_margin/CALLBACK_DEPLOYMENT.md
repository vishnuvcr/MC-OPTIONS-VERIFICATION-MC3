# Paytm Callback Deployment Boundary

## Purpose

Provide a stable HTTPS callback and fixed public IPv4 for the Paytm Money application. This is separate from GitHub Actions because GitHub-hosted runners do not provide a stable application IP suitable for permanent allowlisting.

## Recommended deployment

Use one small Ubuntu VPS/VM with a static public IPv4. AWS Lightsail is one documented option. AWS states that the default public IPv4 can change after restart, while an attached static IPv4 remains fixed.

AWS reference: https://docs.aws.amazon.com/lightsail/latest/userguide/lightsail-create-static-ip.html

## Provisioning sequence

1. Create an Ubuntu instance in AWS Lightsail (or an equivalent VPS in your own account).
2. Attach a Static IPv4 to the instance.
3. Record that public IPv4 as PAYTM_PRIMARY_IP.
4. Allow inbound TCP 22 only from your administration network, and TCP 80/443 for the callback service.
5. Install the repository callback service and a TLS reverse proxy.
6. Use an HTTPS callback URL such as:

   https://paytm-auth.<your-domain>/paytm/callback

7. Put the fixed public IPv4 into the Paytm app Primary IP field.
8. Only populate Secondary IP with a second real fixed public IPv4 if Paytm requires it; do not invent loopback addresses.
9. Verify the callback health endpoint before completing Paytm registration.

## Why this cannot be completed entirely from the repository

The actual public IPv4 is allocated by the user's cloud provider/account. It cannot be predetermined in a research repository and must not be guessed. Cloud credentials must also remain outside GitHub source files.

## Authentication safety

The callback may receive a Paytm request token. It must never write that token, API secret or JWT into application logs. Phase 2 will implement the validated official Paytm SDK authentication flow and store only non-secret audit metadata.

## Paytm app values after provisioning

Use the following fixed values once the server exists:

- App Name: MC OPTIONS
- Product Type: Rule Based Trading Platform
- Redirect URL: https://paytm-auth.<your-domain>/paytm/callback
- Postback: OFF
- Primary IP: <PAYTM_PRIMARY_IP>
- Secondary IP: <PAYTM_SECONDARY_IP if required>

The placeholder values must be replaced by the real server IP/domain. No fabricated IP is permitted.
