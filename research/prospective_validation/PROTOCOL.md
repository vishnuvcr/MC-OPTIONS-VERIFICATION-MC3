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
- Signal target: 09:30 IST.
- Operational capture window: 09:25–09:40 IST, to accommodate GitHub Actions scheduler/provider latency. Every record retains the actual observation timestamp and timing status. Observations outside this window are not accepted as prospective D3 signals.
- Paper execution: current bid/ask snapshot with the research 2-point adverse slippage per execution leg.
- Exit: expiry settlement.
- No live orders are ever submitted by this workflow.

## D3 definition

D3 is the third trading session before the contract's actual expiry session, counting backward over the exchange-specific trading calendar. The contract's expiry field is preferred over inferred weekday rules.

## Prospective firewall

After the first prospective signal, no strike threshold, MC parameter, gate, slippage, lot-size, execution, or exit rule may be tuned using prospective observations.

Manual `force_today` is a diagnostic mode only. It never creates a valid prospective observation or a paper trade.

## Required logs

The system keeps append-only:
- signals: every NIFTY/SENSEX scan, including NOT_D3, timing-invalid, gate-fail, data-error and valid-trade outcomes;
- events: paper entries, repeated live marks and exits;
- errors: every recoverable and fatal data/workflow error;
- runs: workflow run metadata and repository revision;
- snapshots: source-chain snapshots and all material MC inputs used for a valid signal.

## Live marking

Open paper positions are marked every 10 minutes during the configured Indian market window. Long legs are marked conservatively to bid; short legs to ask. If bid/ask is unavailable, LTP is used and the fallback is recorded.

The dashboard reports both gross MTM and an entry-cost-adjusted net MTM estimate. Final expiry P&L also includes the configured expiry STT estimate.

## Costs and capital

The primary research execution friction remains 2 option points of adverse slippage per leg. The inherited Paytm Money-aligned cost schedule is applied as a research cost model for entry and expiry accounting; it is not relabeled as a broker quote unless current account-specific rates are separately verified.

The workflow does not infer actual exchange/SPAN margin from P&L. Margin/capital fields remain separate from risk proxies.

## Data-source hierarchy

1. Official NSE/BSE market data where a machine-readable endpoint is available.
2. Paytm Money market-data endpoints when credentials are configured.
3. Explicitly configured external market-data adapter.
4. Never use fabricated or synthetic market prices in prospective results.

NIFTY currently uses a public NSE option-chain adapter. SENSEX uses a configured BSE/market-data adapter boundary and fails closed when no attributable live option-chain source is configured.

## Acceptance

A prospective observation is valid only when:
- the expiry and D3 date are attributable;
- the actual observed timestamp is inside the 09:30 operational window;
- a source snapshot exists;
- the four tradable strikes are available;
- the MC gate can be calculated from the live signal snapshot;
- paper entry prices are available for all four legs.

A gate-positive observation that cannot obtain executable four-leg quotes is logged as a signal but is not opened as a paper trade.

## Stop rule

This module is an operational validation harness. It does not tune the strategy. Research interpretation is performed only after the pre-registered prospective observation window is complete.
