# RQ-6 Observation Definition Protocol

## Why this matters

“756 historical sessions” can describe different statistical objects. The predecessor implementation operates on transformed returns, not directly on closes.

## Current MC1 implementation

The earliest MC1 module derives logret as log(close_t) minus log(close_{t-1}), filters finite values, and retains the last 756 transformed observations before the D3 signal date.

Therefore 756 usable log returns require 757 underlying closes when the first return is formed by differencing adjacent closes.

## Competing definitions

| ID | Historical object | Nominal count | Required closes | Status |
|---|---|---:|---:|---|
| OBS-A | Last 756 closes | 756 | 756 | Candidate only |
| OBS-B | Last 756 simple returns | 756 | 757 | Candidate only |
| OBS-C | Last 756 log returns | 756 | 757 | Matches MC1 implementation |
| OBS-D | 756 prior sessions including a separate signal anchor | 756 | depends | Candidate only |
| OBS-E | 756 contiguous return observations ending immediately before D3 | 756 | 757 | Candidate only |

## Boundary rule from MC1

MC1 applies the date filter daily date < signal date before computing the log-return series and then selects the last 756 finite returns. This excludes the D3 session close from the historical return sample. The D3 09:30 option snapshot is used for the starting spot and signal prices, not as a daily-close return observation.

## Acceptance test

Any claimed authoritative method must record:
- first observation date;
- last observation date;
- raw close count;
- transformed return count;
- whether D3 is excluded;
- exact ordered observation vector hash;
- whether the previous close is part of the historical sample, only the anchor, or both.

A one-session boundary shift is a distinct model and must be re-evaluated, not treated as a cosmetic implementation detail.
