# Prospective Data-Provider Audit

## NIFTY
The operational adapter currently uses the public NSE option-chain service. The workflow records the provider name and the full source snapshot used for the signal.

## SENSEX
BSE exposes an option-chain web service, and SEBI's exchange-directory page links to the official BSE derivatives option-chain page. The repository does not silently depend on an undocumented BSE endpoint. SENSEX now uses an automatic online unofficial indiaopt BSEClient adapter by default, with a configured normalized live-chain adapter retained as an override.

A current public open-source project demonstrates automated BSE SENSEX option-chain polling through indiaopt and BSE scrip code 999920. PyPI describes indiaopt as an NSE/BSE market-data library. These are third-party integrations, not authoritative exchange definitions. citeturn3search0turn0search3

## Paytm Money
Paytm Money documentation exposes authenticated market-data APIs. The prospective module keeps a credential boundary for a broker-grade market-data adapter, but no live broker order endpoint is called.

## Decision
For prospective validation, data provenance takes priority over silently filling gaps. The SENSEX provider order is: configured normalized feed if supplied, otherwise unofficial indiaopt online retrieval; provider failure is logged as unavailable rather than replaced with synthetic or inferred prices. Accepted observations store provider/version/scrip/expiry provenance.

## Current authoritative references reviewed — 2026-09-22

- NSE F&O 2026 trading-holiday circular NSE/FAOP/71777: https://nsearchives.nseindia.com/content/circulars/FAOP71777.pdf
- NSE F&O Jan 15, 2026 additional holiday circular NSE/FAOP/72262: https://nsearchives.nseindia.com/content/circulars/FAOP72262.pdf
- NSE option settlement price: https://www.nseindia.com/static/products-services/equity-derivatives-settlement-price
- NSE STT rates from Apr 1, 2026: https://www.nseindia.com/static/products-services/equity-derivatives-securities-transaction-tax
- NSE equity-options transaction-charge circular FA73061: https://nsearchives.nseindia.com/content/circulars/FA73061.pdf
- Paytm Money current F&O FAQ states Rs.10 per unique executed order, while Paytm Money's 2025 pricing announcement states flat Rs.20 across segments from Jan 15, 2025. Because public Paytm material is not internally consistent about the current account-specific rate, the validation engine keeps brokerage configurable rather than silently asserting a single universal live rate.


## PV-13 runtime choice — 2026-09-22
The repository now installs `indiaopt>=0.1.1,<0.2` and calls `BSEClient.fetch_option_chain("999920", is_index=True)` automatically. The normalized adapter accepts the provider's strike-level CE/PE LTP fields and optional bid/ask fields. If bid/ask are absent, the locked engine LTP fallback and adverse slippage rule remain in force. This is a research-data compromise, not a claim of broker-grade execution quality.

The separate `bse-options` package was reviewed as corroborating unofficial BSE-chain tooling but is not required by the runtime. citeturn5search0
