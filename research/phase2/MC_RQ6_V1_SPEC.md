# MC-RQ6-v1 — Traceable Monte Carlo Control Specification

## Provenance status

This is the exact Monte Carlo control reconstructed from the earliest MC1 project implementation. It is authoritative for reproducing the predecessor project implementation, but external originality of the BATMAN method remains unverified.

## Historical observation set

For each D3 signal date:
1. keep daily observations with date strictly before D3;
2. compute log returns from adjacent daily closes;
3. drop the first NaN created by differencing and any non-finite values;
4. take the final 756 finite log-return observations.

Therefore the method requires 757 close observations to create 756 adjacent log returns when no additional missing-value filtering occurs.

## Future horizon

The expiry session function returns D3 signal, D2, D1 and expiry. The engine therefore simulates 3 future daily-return steps from the D3 signal anchor to the expiry terminal value.

## Path sampling

For each path and each future step, draw an integer index uniformly from 0 through 755 with replacement using NumPy default_rng(seed=756). Draws are independent across future steps conditional on the RNG stream; no block or without-replacement dependence is imposed.

## Path transformation

For sampled log returns r1, r2 and r3 and starting spot S0:

S_T = S0 * exp(r1 + r2 + r3)

## Starting spot at D3 09:30

The option dataset is restricted to timestamps at or before 09:30 IST on D3, and the latest available timestamp is selected. The preferred S0 is the median call-put-parity estimate K + CE - PE for strikes within 2% of the previous close. If no valid parity estimate exists, the previous close is used as fallback.

This is not equivalent to blindly using a raw index tick exactly at 09:30.

## Terminal quantiles

Compute empirical terminal-spot quantiles at 0.20, 0.35, 0.65 and 0.80.

## Tradable strike map

Map each continuous target to the nearest available strike on the correct option side while ensuring all four selected strikes are unique. Ties resolve to the lower strike.

## Locked four-leg portfolio

+1 P35 PE
-2 P20 PE
+1 P65 CE
-2 P80 CE

## Gate and execution

Gross MC-EV is mean terminal portfolio payoff less the signal premium cashflow. Trade eligibility requires gross MC-EV > 0. Execution is the first common executable observation after the signal time.

## Research identity rule

Any future implementation claiming MC-RQ6-v1 identity must match the fixed observation vector, seed, path count, horizon, starting spot, and resulting terminal array hash under the same software versions.
