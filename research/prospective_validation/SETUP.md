# Setup

## GitHub Actions
The workflows require:
- Actions read/write repository permission so workflow runs can append logs;
- Pages enabled with the **GitHub Actions** source.

## Optional secrets
For SENSEX or a preferred broker-grade market-data provider, configure:
- `PAYTM_MONEY_JWT_TOKEN` for Paytm Money authenticated market-data adapters when enabled;
- `PAYTM_MONEY_BROKERAGE_PER_ORDER` to override the default ₹20 research brokerage assumption with the actual account-specific rate;
- `BSE_OPTION_CHAIN_URL` for an explicitly configured normalized BSE option-chain endpoint.

The code never stores these secrets in the repository.

## Recommended first run
Use the manual **BATMAN PAPER TRADE** workflow with `mode=scan` after verifying the market-data configuration. A failed or missing provider is logged rather than silently replaced with synthetic prices.

## Marking cadence
The live-mark workflow runs every 10 minutes on weekdays and is guarded by Indian market hours. GitHub Actions schedules are best-effort, so the dashboard records the actual observation timestamp and does not pretend a scheduled run happened at an exact wall-clock second.

## Current data-source references
- NSE option chain: https://www.nseindia.com/option-chain
- NSE contract information: https://www.nseindia.com/static/products-services/equity-derivatives-contract-information
- Paytm Money Open API: https://developer.paytmmoney.com/
- Paytm Money historical minute market-data API: https://developer.paytmmoney.com/docs/api/historical-api-beta
- BSE market-data service: https://marketdata.bseindia.com/

## GitHub Pages

Enable **Settings → Pages → Build and deployment → Source: GitHub Actions** once for the repository. The workflows already build and deploy the static portal.

## SENSEX data

The default SENSEX path intentionally fails closed unless `BSE_OPTION_CHAIN_URL` is configured to an attributable JSON feed containing at least `expiry`, `strike`, `option_type`, `ltp`, `bid`, and `ask`. The official BSE market-data service is subscription/registration based, so no unofficial scraping fallback is silently enabled.
