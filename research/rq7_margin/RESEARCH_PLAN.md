# RQ-7 Research Plan — Actual Capital / Margin Reduction Using Attributable Broker Data

## Research question

Can attributable Paytm Money and exchange data be used to reconstruct the actual capital/margin required by the locked BATMAN MC-RQ6-v1 four-leg NIFTY and SENSEX option strategy, and can parameter changes reduce required capital/margin without relying on ES95/ES99 as a substitute for actual margin?

## Why this is a new research

RQ-6 verified and froze the Monte Carlo path-generation control. The present research starts again at Phase 1, in the same repository, because the unresolved objective is total trading capital/margin reduction by changing strategy parameters rather than merely reducing a risk proxy.

All prior RQ-6 and prospective-validation phases remain intact. This research must not overwrite their historical results.

## Hypotheses

- H0: Within the preregistered parameter space and execution constraints, parameter changes do not produce a reproducible reduction in attributable required trading capital/margin while meeting predefined economic and risk constraints.
- H1: At least one parameter configuration produces a reproducible reduction in attributable required trading capital/margin while meeting predefined constraints.

The study will not declare a configuration successful merely because it has a lower proxy risk measure.

## Primary outcome

1. Attributable required trading capital/margin in INR, separated into exchange/clearing margin, broker upfront/available margin, premium cash requirement for long legs, and other documented blocked funds.

## Secondary outcomes

- net P&L after brokerage, statutory charges and slippage;
- margin-to-net-P&L ratio;
- peak capital usage;
- capital efficiency;
- win rate;
- drawdown;
- ES95/ES99 and stress loss as secondary risk measures only;
- gate rate and trade frequency;
- execution feasibility;
- margin variability by expiry and market regime.

## Locked control

MC-RQ6-v1 remains unchanged: final 756 finite daily log returns strictly before D3; IID with-replacement sampling; NumPy default_rng(seed=756); 5,000 paths in prospective validation; 3-session horizon; P20/P35/P65/P80; +1 P35 PE, -2 P20 PE, +1 P65 CE, -2 P80 CE; gross MC-EV > 0 gate; 09:30 IST target; 2 option points adverse slippage per execution leg; historical lot size; brokerage and STT; paper-only operational layer.

## Parameter space

Phase 1 will define and preregister parameter families before outcome evaluation. Candidate families include terminal quantile geometry, wing/body distance, long/short quantity ratio where margin rules permit, strike-spacing constraints, and expiry-selection variants where scientifically justified. Execution and cost assumptions are sensitivity dimensions, not optimization targets.

No parameter will be selected from the final evaluation sample.

## Phase map

### Phase 1 — Broker/exchange authority recovery and connectivity
- Recover current Paytm Money authentication, market-data, margin and account-data capabilities from authoritative documentation and official SDKs.
- Establish whether live broadcast provides option LTP/quote/full-depth data for NSE and BSE.
- Establish whether historical API provides attributable NIFTY and SENSEX option histories sufficient for backtesting.
- Establish exact broker margin endpoints, request fields, response fields and whether they provide order/scrip margin rather than only current-account state.
- Establish exchange/SPAN sources for historical margin where broker APIs cannot reconstruct historical requirements.
- Build a secure callback/authentication deployment boundary.
- Define secret names and never store credentials in Git.
- Acceptance: authority matrix and executable connectivity design; no unverified endpoint assumptions.

### Phase 2 — Attributable margin-data capture
- Authenticate without exposing credentials.
- Capture instrument/security master and contract metadata.
- Capture option quotes/bid-ask and historical data.
- Capture broker margin responses for representative four-leg BATMAN orders and parameter variants.
- Capture account-specific brokerage/charges.
- Cache raw responses with timestamps, source, request hash and schema.
- Acceptance: reproducible raw-data fixtures and provenance ledger.

### Phase 3 — Margin reconstruction and parameter grid
- Reconstruct actual capital/margin for the locked control.
- Evaluate the preregistered parameter grid on the same expiry set.
- Compute required capital/margin, net P&L and capital efficiency.
- Separate initial, peak and expiry capital usage.
- Include slippage, brokerage, STT and lot size.
- Acceptance: complete control-vs-parameter margin ledger.

### Phase 4 — Walk-forward and robustness
- Freeze parameter selection using training windows only.
- Evaluate chronologically held-out periods.
- Repeat across NIFTY and SENSEX.
- Stratify by volatility/regime where attributable data permit.
- Bootstrap expiry clusters and use paired inference.
- Stress costs, liquidity and margin snapshots.
- Acceptance: out-of-sample capital-reduction estimate with uncertainty interval.

### Phase 5 — Combined manuscript and control decision
- Integrate RQ-7 with the retained RQ-6 manuscript without rewriting historical results.
- Produce complete manuscript, figures, tables, appendices and supplementary material.
- State exactly whether actual margin reduction was demonstrated, not merely proxy reduction.
- Freeze any validated parameter set as a prospective candidate; otherwise retain MC-RQ6-v1 as control.
- Acceptance: reproducible final research package.

## Statistical methodology

Primary: paired expiry-level difference in required capital/margin; paired bootstrap confidence intervals clustered by expiry; mean and median margin reduction; paired sign-flip/permutation tests; capital-efficiency ratios with bootstrap intervals.

Secondary: drawdown, ES95/ES99, win-rate differences, gate-rate differences, strike-switch frequency, execution failure rate, and regime-stratified effects.

Multiplicity: all tested parameter families and comparisons will be enumerated before evaluation; no cherry-picked parameter will be presented as confirmatory evidence.

## Data hierarchy

1. Paytm Money attributable API/account data.
2. Official NSE/BSE/exchange or clearing margin data.
3. Official exchange contract specifications.
4. Validated public mirrors only where attributable provenance is retained.

No synthetic live market prices or fabricated margin values are permitted.

## Security

API keys, API secrets, request tokens and JWT/access tokens must never enter Git. GitHub Actions Secrets are the intended CI secret store. Authentication callback must run on a controlled HTTPS endpoint with a fixed public IP if Paytm requires IP allowlisting. The research system remains paper-only; enabling the Paytm Trading API does not authorize this repository to place live orders.

## Non-repeat rules

Never call ES95/ES99 an actual broker margin figure. Never use a current margin response as historical margin without timestamped evidence. Never optimize parameters on the final evaluation period. Never substitute LTP for bid/ask when execution feasibility is being tested without recording the substitution. Never expose credentials in chat, screenshots or repository files. Never enable live order submission as part of this research.
