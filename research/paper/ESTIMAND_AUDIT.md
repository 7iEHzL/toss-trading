# Estimand and Hypothesis Audit

## Original Identity

`R = Σ b*s*r + Σ(w-b)*s*r - c`

| Object | Classification | What it identifies |
|---|---|---|
| `Σw*s*r-c` | Accounting identity | Realized strategy return under chosen rules |
| `Σb*s*r` | Descriptive attribution / counterfactual if tradable | Direction payoff under fixed reference weights |
| `Σ(w-b)*s*r` | Descriptive residual | Allocation deviation mechanically conditional on signal; not pure allocation value |
| `c` | Accounting estimate | Cost under the chosen cost model, not necessarily historical realized cost |

The second term does not isolate allocation and interaction separately.

## Better Factorial Counterfactual

Define two signal states and two allocation rules on identical returns:

- `P11 = Σ w_t s_t r_t`: dynamic signal, dynamic allocation
- `P10 = Σ b s_t r_t`: dynamic signal, fixed allocation
- `P01 = Σ w_t q r_t`: fixed reference exposure `q`, dynamic allocation
- `P00 = Σ b q r_t`: fixed exposure, fixed allocation

Then define descriptive factorial contrasts:

- Signal contrast: `P10-P00`
- Allocation contrast: `P01-P00`
- Interaction: `P11-P10-P01+P00`

These are counterfactual estimands only if all four portfolios are defined ex ante and risk matched.
They remain non-causal because signal and allocation states are not randomized.

## Hypothesis Separability

- H1: estimable from `P10-P00` and panel signal coefficients.
- H2: estimable from `P01-P00`, but depends critically on reference exposure `q`.
- H3: estimable as difference-in-differences above.
- Verdict: `CONDITIONAL`; separable algebraically, not causally, and only after freezing `b`, `q`,
  leverage and volatility normalization independently of outcomes.

## Primary Stability Design

Recommend continuous state-variable interaction as primary, using one mechanism selected from
external theory before data. It avoids assuming a break and retains information. Fixed-date and
unknown-break tests are diagnostics; rolling estimates are descriptive; subsamples are robustness.

| Design | Advantage | Problem | Data-mining risk | Defensibility |
|---|---|---|---|---|
| Fixed ex-ante date | Simple | Date needs external rationale | Medium | Medium if literature-based |
| Unknown break | Detects change | Low power and date search | High | Diagnostic only |
| Rolling/expanding | Shows evolution | Noisy overlapping estimates | High | Descriptive only |
| Continuous state interaction | Tests mechanism without assuming break | State may be endogenous | Low if externally fixed | Best primary option |
| Subsamples | Transparent | Wastes information | High after inspection | Robustness only |

## Sample Feasibility

Nine ETFs × sixteen years is inadequate: effectively nine assets, four broad clusters and roughly
192 monthly observations before overlap/common-shock adjustment. A reasonable target is 40+ years,
50–100 contracts, four asset classes with multiple independent markets, and enough contract-level
history for block inference. This is a design target, not a calculated power guarantee. Formal power
requires assumed effect size, dependence and break magnitude.
