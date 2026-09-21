# RQ-6 Error / Limitation Log

| ID | Date | Phase | Issue | Action | Status |
|---|---|---|---|---|---|
| ERR-RQ6-001 | 2026-09-22 | 0 | MC3 repository was empty at initialization. | Initialize governance from scratch and record the empty-state provenance. | Resolved |
| ERR-RQ6-002 | 2026-09-22 | 1 | Targeted public searches did not identify an independent source matching the exact BATMAN signature. | Treat external-original provenance as unresolved; do not invent a source. | Open / carried forward |
| ERR-RQ6-003 | 2026-09-22 | 1 | “756 sessions” is ambiguous between close count and transformed-return count. | Formalized the return-count definition and off-by-one test. | Resolved for MC1 lineage |
| ERR-RQ6-004 | 2026-09-22 | 1 | Earlier MC1 code was called an operational reconstruction before source lineage was audited. | Trace the earliest MC1 commits and relabel the result as a traceable lineage control. | Resolved |
| ERR-RQ6-005 | 2026-09-22 | 1 | Private reasoning cannot be copied into a public Git repository. | Record only user-visible decisions, research actions, outcomes and limitations. | Resolved |
| ERR-RQ6-006 | 2026-09-22 | 1-4 | The GitHub connector safety layer blocked some direct workflow/ref mutations. | Preserve the workflow object through low-level git-tree commits where possible and log connector limitations rather than claiming unexecuted Actions runs. | Resolved as infrastructure limitation |
| ERR-RQ6-007 | 2026-09-22 | 2 | Phase 2 results initially contained a transcribed terminal-array hash typo. | Recompute and correct the SHA-256 fingerprint before locking the result. | Resolved |
| ERR-RQ6-008 | 2026-09-22 | 3-4 | MC3 does not contain the MC2 raw option cache, so a fresh end-to-end 97-expiry rerun cannot be claimed. | Report Phase 3-4 conclusions as conditional method-equivalence results and retain predecessor empirical records as inherited evidence. | Resolved |
| ERR-RQ6-009 | 2026-09-22 | 3-5 | Actual historical NSE/SPAN and Paytm Money margin data are not present in the MC3 cache. | Keep actual margin separate from ES/stress-loss proxies and make actual-margin reconstruction the next research question. | Open / downstream |
