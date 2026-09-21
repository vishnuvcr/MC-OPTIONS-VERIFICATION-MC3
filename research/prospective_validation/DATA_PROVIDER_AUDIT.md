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
