# RQ-6 Conversation / Decision Log

## 2026-09-22 — User request

The user requested a new research track in MC3 for RQ-6: verify whether the exact authoritative 756-session BATMAN Monte Carlo path-generation method changes baseline economics, strike selection, capital/risk profile or previous Phase 3-4 conclusions. The user specified the primary H0/H1 and required sub-questions and asked that the corrected method become the locked control for later margin-reduction research.

## 2026-09-22 — Repository audit

MC3 was initially empty. Prior research was therefore not present in MC3 and was not overwritten. MC1 and MC2 were audited as predecessor provenance sources.

## 2026-09-22 — Methodological decision

The MC1 Monte Carlo transformation was treated as an operational reconstruction until source lineage was audited.

## 2026-09-22 — Lineage finding

The earliest MC1 Monte Carlo implementation was identified in commit 20b606a015a54b08f77e088faf74aae7df7ed5cf, which added src/model/mc.py. The earliest strategy functions are in 43ec07c9a29d1c8429c2542b6dfce0497ee7c2c4 and the first trade engine is in 63ff284d0b5a1ed211ff85845d02c13cc038b024.

## 2026-09-22 — Observation and sampler decision

The traceable implementation uses the final 756 finite daily log returns strictly before D3, not 756 closes. It samples individual returns with replacement for each future step using NumPy default_rng(756) and compounds them in log-return space.

## 2026-09-22 — Anchor decision

The D3 09:30 starting spot is the latest option snapshot at or before 09:30 IST, with a preferred call-put-parity median within a 2% band around previous close and previous close fallback.

## 2026-09-22 — Exact-control decision

MC-RQ6-v1 was locked as the traceable predecessor control, with deterministic fixture SHA-256 6f64abfc0c9d6f9e4e65f52fb47c6f837f208f963cbf05871cb15db8c8626677.

## 2026-09-22 — Downstream decision

Because MC-RQ6-v1 is functionally identical to the earliest MC1 implementation, replacing the label “operational reconstruction” with the exact traceable control produces no mathematical change under identical inputs. The prior Phase 3-4 evidence is therefore method-stable conditional on using the same MC1-lineage sampler. MC3 does not claim a fresh MC2 raw-data backtest because that historical cache is not present in MC3.

## 2026-09-22 — Final research decision

Lock MC-RQ6-v1 as the control for subsequent margin-reduction research. Move the next research question to actual entry and peak capital/margin reconstruction, with NSE/SPAN and Paytm Money attributable data, while retaining the predecessor strike-frontier and walk-forward results.
