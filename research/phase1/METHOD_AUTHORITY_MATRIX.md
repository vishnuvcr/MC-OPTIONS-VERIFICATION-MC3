# RQ-6 Method Authority Matrix

| Component | MC1 evidence | Evidence strength | Authority status |
|---|---|---|---|
| Historical window | Earliest mc.py filters daily date < signal date, forms daily log returns, then retains last 756 finite values. | Direct source-code lineage | Operationally established |
| Observation count | 756 transformed log returns; ordinarily 757 closes are needed to form them. | Direct source-code lineage | Operationally established |
| Sampling | NumPy integer indices sampled with replacement for every future horizon step. | Direct source-code lineage | Operationally established |
| Dependence | No serial dependence is imposed by the sampler; sampled returns are independently indexed conditional on the fixed RNG stream. | Direct source-code lineage | Operationally established |
| Horizon | Engine passes len(expiry_sessions)-1 = 3 future daily steps for D3-to-expiry. | Direct source-code lineage | Operationally established |
| Starting spot | Option snapshot uses latest timestamp <= 09:30 IST. signal_spot_from_parity prefers median same-strike call-put parity in a 2% band around the previous close; previous close is fallback. | Direct source-code lineage | Operationally established; wording “D3 09:30 anchor” is incomplete |
| RNG | NumPy default_rng with seed 756 in the operational reconstruction. | Direct source-code lineage | Operationally established for MC1, not original-authority proof |
| Terminal transform | S0 multiplied by exp(sum(sampled log returns)). | Direct source-code lineage | Operationally established |
| Terminal quantiles | NumPy empirical quantiles at 0.20, 0.35, 0.65, 0.80 of terminal spots. | Direct source-code lineage | Operationally established |
| Strike mapping | Nearest available strike, unique across the four targets, deterministic lower-strike tie break; PE targets map to PE grid and CE to CE grid. | Direct source-code lineage | Operationally established |
| Four legs | +1 P35 PE, -2 P20 PE, +1 P65 CE, -2 P80 CE. | Locked strategy spec and earliest code | Locked strategy, not independent MC authority |
| Gate | Gross MC-EV > 0 before execution. | Early engine + later workflow | Locked strategy |
| External original source | No matching public source found in targeted searches to date. | Negative search evidence | Unresolved |

## Key interpretation

The predecessor model is not an underspecified black box: its implementation can be reconstructed exactly from the MC1 commit lineage. The unresolved question is different and narrower: whether this implementation is the same as the original BATMAN implementation referred to by the project description.

That distinction controls whether Phase 3–4 results can be called a revalidation of the original strategy or only a revalidation of the predecessor reconstruction.
