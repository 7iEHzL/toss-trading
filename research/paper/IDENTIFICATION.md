# Identification and Mathematical Decomposition

## Objects

For asset `i` and decision date `t`, let `s_it` be the frozen direction signal, `w_it` the
ex-ante dynamic allocation, `b_i` a fixed reference allocation, `r_i,t+1` the next-period excess
return, and `c_t` implementable trading cost.

`R_t+1 = Σ_i w_it s_it r_i,t+1 - c_t`

Using `w_it = b_i + (w_it - b_i)` gives the accounting identity:

`R_t+1 = Σ_i b_i s_it r_i,t+1 + Σ_i (w_it-b_i)s_it r_i,t+1 - c_t`

- First term: fixed-allocation directional component.
- Second term: allocation deviation including signal-allocation interaction.
- Third term: costs.

This is a mathematical identity, not causal identification. A matched-volatility counterfactual
compares portfolios normalized to the same ex-ante and realized risk. Regression coefficients are
econometric estimates and require maintained assumptions stated separately.

## Competing Explanations and Discriminating Tests

| Explanation | Test | Remaining limitation |
|---|---|---|
| Directional predictability | Panel next-return regression on lagged signal | Signal may proxy for time-varying expected return |
| Positive unconditional returns | Compare signal rule with always-long matched-risk portfolio | Counterfactual still depends on reference weights |
| Volatility timing | Scaled versus unscaled matched-volatility spanning test | Volatility forecast error |
| Correlation changes | Add ex-ante covariance allocation and fixed correlation-state interactions | State is not causal |
| Leverage/scaling | Enforce identical gross exposure and risk targets | Financing constraints remain |
| Crisis convexity | Externally dated events and continuous drawdown-path variables | Few independent crises |
| Rebound/reversal | Pre-defined rebound speed interaction | Endogenous event classification risk |
| Transaction costs | Frozen cost curves and turnover decomposition | Historical bid-ask data may be unavailable |
| Asset composition | Balanced panel and leave-class-out diagnostic | Reduced breadth/power |
| Sample regimes | Pre-specified and unknown-break tests | Break detection is descriptive without mechanism |

## Identification Claim Allowed

The design can identify statistical instability in matched component payoffs conditional on its
data and model. It cannot identify a causal macroeconomic regime effect without an external source
of variation. R5's two periods cannot be used as a publication break definition.
