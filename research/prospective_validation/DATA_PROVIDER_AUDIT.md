# Prospective Data-Provider Audit

## NIFTY
The operational adapter currently uses the public NSE option-chain service. The workflow records the provider name and the full source snapshot used for the signal.

## SENSEX
BSE exposes an option-chain web service, and SEBI's exchange-directory page links to the official BSE derivatives option-chain page. The repository does not silently depend on an undocumented BSE endpoint. SENSEX therefore uses a configured normalized live-chain adapter and fails closed when one is not configured.

A current public open-source project demonstrates automated BSE SENSEX option-chain polling through the indiaopt library and BSE scrip code 999920, while PyPI describes the bse-options package as an unofficial BSE option-chain API. These sources are treated as integration leads, not as authoritative exchange definitions.

## Paytm Money
Paytm Money documentation exposes authenticated market-data APIs. The prospective module keeps a credential boundary for a broker-grade market-data adapter, but no live broker order endpoint is called.

## Decision
For prospective validation, data provenance takes priority over silently filling gaps. Missing SENSEX live quotes are logged as unavailable rather than replaced with synthetic or inferred prices.

## Current authoritative references reviewed — 2026-09-22

- NSE F&O 2026 trading-holiday circular NSE/FAOP/71777: https://nsearchives.nseindia.com/content/circulars/FAOP71777.pdf
- NSE F&O Jan 15, 2026 additional holiday circular NSE/FAOP/72262: https://nsearchives.nseindia.com/content/circulars/FAOP72262.pdf
- NSE option settlement price: https://www.nseindia.com/static/products-services/equity-derivatives-settlement-price
- NSE STT rates from Apr 1, 2026: https://www.nseindia.com/static/products-services/equity-derivatives-securities-transaction-tax
- NSE equity-options transaction-charge circular FA73061: https://nsearchives.nseindia.com/content/circulars/FA73061.pdf
- Paytm Money current F&O FAQ states Rs.10 per unique executed order, while Paytm Money's 2025 pricing announcement states flat Rs.20 across segments from Jan 15, 2025. Because public Paytm material is not internally consistent about the current account-specific rate, the validation engine keeps brokerage configurable rather than silently asserting a single universal live rate.
