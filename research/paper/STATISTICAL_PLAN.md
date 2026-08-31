# Statistical Plan — Design Only

| Method | Why needed | Hypothesis | Assumptions | Limitation |
|---|---|---|---|---|
| HAC/Newey-West mean and regression SE | Serially correlated overlapping signals | H1-H3 | Weak dependence; valid bandwidth | Sensitive to bandwidth and small samples |
| Asset/time two-way clustered SE | Shared shocks and repeated assets | H1-H3 | Enough independent clusters | Few asset classes weaken inference |
| Stationary/block bootstrap | Non-normal strategy and Sharpe distributions | H1-H3 | Blocks preserve dependence | Block-length choice |
| Ledoit-Wolf-type Sharpe difference CI | Avoid raw Sharpe comparison | H2 | Stationarity within tested segment | Breaks undermine segment stationarity |
| Sup-Wald/Bai-Perron unknown-break diagnostic | Detect unannounced coefficient changes | H1-H3 | Sufficient observations; stable error process | Date search needs critical-value control |
| Pre-specified interaction regression | Test economically defined states | H1-H3 | State measured without look-ahead | Association is not causality |
| Factor/spanning regression | Separate known risk exposures | H2 | Factors adequately span risks | Model misspecification |
| Holm correction for primary family | Control three primary hypotheses | H1-H3 | Pre-defined family | Reduces power |

Primary design preference: continuous state variables plus a literature-based pre-specified split
if one exists. Unknown-break tests are diagnostics, not a device for choosing a profitable period.
Rolling plots are descriptive only. No break date may be selected from R5 performance.
