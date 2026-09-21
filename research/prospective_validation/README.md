# BATMAN PAPER TRADE — Prospective Validation

This module is the clean prospective-validation layer for the locked MC-RQ6-v1 BATMAN strategy.

### What it does
- scans automatically for NIFTY and SENSEX D3 sessions;
- logs every scan and signal, including gate failures and data failures;
- opens paper positions only when the frozen MC-EV gate is positive and all four legs are executable;
- marks open paper positions frequently from live prices;
- closes positions at expiry using settlement/intrinsic value;
- stores append-only machine-readable logs;
- builds an attractive GitHub Pages dashboard;
- supports a manual workflow named **BATMAN PAPER TRADE**.

### Important
No workflow in this module submits live orders to Paytm Money or any other broker.

For NIFTY, the default market-data adapter uses the public NSE option-chain service. SENSEX live option data requires a configured adapter/credential; the system fails closed and logs DATA_UNAVAILABLE when it cannot obtain attributable live option data.

See [setup](SETUP.md) and [protocol](PROTOCOL.md).
