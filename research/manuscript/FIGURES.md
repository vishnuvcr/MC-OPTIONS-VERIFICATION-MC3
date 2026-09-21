# RQ-6 Figures and Charts

These figures are inherited descriptive evidence from MC2. They are not a new independent MC3 raw-data backtest.

## Figure 1 — Walk-forward candidate-minus-baseline

~~~mermaid
xychart-beta
    title "2026 candidate minus baseline"
    x-axis [Split-A, Split-B]
    y-axis "Rupees per common-gated trade" -500 --> 500
    bar [-161.18, 266.12]
~~~

Intervals:
- Split A: 95% paired bootstrap CI [-818.18, +334.65]
- Split B: 95% paired bootstrap CI [-914.74, +1,270.04]

## Figure 2 — Inherited ES99 proxy comparison

~~~mermaid
xychart-beta
    title "Inherited ES99 proxy"
    x-axis [Baseline, P22-P33-P67-P78]
    y-axis "Rupees" 0 --> 14000
    bar [12706.60, 12130.41]
~~~

Approximate reduction in the inherited proxy: 4.53%.

## Figure 3 — RQ-6 method identity logic

~~~mermaid
flowchart LR
A[756 finite log returns before D3] --> B[IID sampling with replacement]
B --> C[3 future steps]
C --> D[S0 times exp sum returns]
D --> E[P20 P35 P65 P80]
E --> F[Nearest unique listed strikes]
F --> G[Gross MC-EV gate]
~~~
