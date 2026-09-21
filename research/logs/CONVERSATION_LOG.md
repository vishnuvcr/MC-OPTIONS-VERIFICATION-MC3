# RQ-6 Conversation / Decision Log

## 2026-09-22 — User request

The user requested a new research track in MC3 for RQ-6: verify whether the exact authoritative 756-session BATMAN Monte Carlo path-generation method changes baseline economics, strike selection, capital/risk profile or the previous Phase 3–4 conclusions. The user specified the primary H0/H1 and seven sub-questions, and requested that the corrected method become the locked control for later margin-reduction research.

## 2026-09-22 — Repository audit decision

MC3 was initially empty. Prior research was therefore not present in MC3 and was not overwritten. MC1 and MC2 were audited as predecessor provenance sources.

## 2026-09-22 — Methodological decision

The MC1 Monte Carlo transformation is treated as an operational reconstruction until source provenance or reproducible original output establishes authority.

## 2026-09-22 — Lineage finding

The earliest MC1 Monte Carlo implementation was identified in commit 20b606a015a54b08f77e088faf74aae7df7ed5cf, which added src/model/mc.py. Its parent sequence shows the locked strategy functions in commit 43ec07c9a29d1c8429c2542b6dfce0497ee7c2c4 and the first trade engine in commit 63ff284d0b5a1ed211ff85845d02c13cc038b024.

The earliest implementation therefore provides direct evidence for what MC1 actually executed, but not independent evidence that this was the original external BATMAN implementation.

## 2026-09-22 — Anchor finding

The earliest trade engine calls the option-snapshot-based signal_spot_from_parity function using the latest option observation at or before 09:30 IST. The preferred starting spot is the median same-strike call-put parity estimate in a 2% strike band around the previous close; the previous close is only a fallback. This is materially more specific than the simplified phrase “anchored at D3 09:30”.
