# BATMAN Prospective Validation Protocol

## Purpose
Run the locked BATMAN strategy prospectively on genuinely unseen NIFTY and SENSEX expiries, without changing the strategy while validation is running.

## Frozen strategy
- Model: MC-RQ6-v1.
- History: final 756 finite daily log returns strictly before D3.
- Paths: 5,000.
- Seed: 756.
- Horizon: 3 trading-session steps from D3 to expiry.
- Quantiles: P20 / P35 / P65 / P80.
- Position: +1 P35 PE, -2 P20 PE, +1 P65 CE, -2 P80 CE.
- Gate: gross MC-EV > 0.
- Signal time: 09:30 IST.
- Paper execution: immediate post-signal live bid/ask snapshot, with the research 2-point adverse slippage per execution leg.
- Exit: expiry settlement.
- No live orders are ever submitted by this workflow.

## D3 definition
D3 is the third trading session before the contract's actual expiry session, counting backward over the exchange-specific trading calendar.

## Prospective firewall
After the first prospective signal, no strike threshold, MC parameter, gate, slippage, lot-size, execution, or exit rule may be tuned using prospective observations.

## Required logs
The system keeps append-only:
- signals: every NIFTY/SENSEX scan, including no-trade outcomes;
- events: paper entries, marks and exits;
- errors: every recoverable and fatal data/workflow error;
- runs: workflow run metadata and data-source provenance;
- snapshots: D3 source snapshots for selected option contracts and full NIFTY chain snapshots when available.

## Live marking
Open paper positions are marked every 10 minutes during the Indian cash-market window. Long legs are marked conservatively to bid; short legs to ask. If bid/ask is unavailable, LTP is used and the log records the fallback.

## Data-source hierarchy
1. Official NSE/BSE market data where a machine-readable endpoint is available.
2. Paytm Money market-data endpoints when credentials are configured.
3. Explicitly configured external market-data adapter.
4. Never use fabricated or synthetic market prices in prospective results.

A missing live source causes a logged DATA_UNAVAILABLE result, not a simulated trade.

## Acceptance
A prospective observation is valid only when:
- the expiry and D3 date are attributable;
- a source snapshot exists;
- the four tradable strikes are available;
- the MC gate can be calculated from the live signal snapshot;
- paper entry prices are available for all four legs.

## Stop rule
This module is an operational validation harness. It does not tune the strategy. Research interpretation is performed only after the pre-registered prospective observation window is complete.
