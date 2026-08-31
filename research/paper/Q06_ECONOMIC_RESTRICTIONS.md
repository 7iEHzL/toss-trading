# Q06 Economic-restrictions Audit

## Required form

A Level-3 restriction must be fixed before results and connect an economic characteristic `Z_i` to
the sign or magnitude of

`Delta beta_i = beta_i(revised macro) - beta_i(real-time macro)`.

It is not enough that factor `i` is cyclical. The literature must also explain why statistical-agency
revision error loads differentially on that exposure.

## Candidate mechanisms red-teamed

| Candidate `Z` | Literature-supported first link | Missing bridge to agency revision | Ex ante? | Falsifiable? | Valid Q06 restriction? |
|---|---|---|---:|---:|---:|
| Financing constraints of factor legs | He–Su–Yu predict heterogeneous responses to subjective productivity-belief revisions | Agency revisions do not themselves cause investor optimism, financing or overinvestment at the historical return date | Yes for beliefs | Yes | **No** |
| Business-cycle exposure | Value, momentum and other factors have documented heterogeneous recession/macro exposures; Vincenz–Zeissler summarize factor-predictor links | Exposure to the true cycle does not determine covariance with later measurement error or benchmark revisions | Broadly | Broadly | **No** |
| Cash-flow versus discount-rate duration | Duration-based factor theories predict heterogeneous discount-rate sensitivity | No inspected paper maps duration to the sign of later statistical revisions | Potentially | Yes | **No** |
| Investment/production linkage | Production-based asset pricing links characteristics to investment shocks | It does not predict which factor's conditional coefficient is most changed by agency re-estimation | Potentially | Yes | **No** |
| Macro-announcement sensitivity | Announcement literature documents heterogeneous asset responses to surprises | Initial-release news sensitivity is distinct from covariance with revisions occurring later | Yes | Yes | **No** |
| Direct exposure to the revision component | Ghysels' decomposition mechanically implies larger gaps when returns covary with revision components | `Z` is the outcome being explained, not an independent economic characteristic | Yes | Yes | **Tautological** |
| Factor composition | Factor legs differ in size, value, profitability, investment and constraints | Composition alone supplies no signed mapping to statistical revision error | Yes | Yes | **No** |

## Strongest plausible restriction

The strongest literature-grounded economic ordering is He–Su–Yu's financing-constraint ordering:
belief upgrades should affect constrained factor legs more strongly. It is a valid prediction for
**subjective expectation revisions**. It is not a valid prediction for **statistical-agency data
revisions**, because those later revisions were not in agents' information sets and need not induce the
financing/overreaction channel.

Using this ordering in Q06 would silently change the treatment from MacroVintage to macro beliefs, or
would assume the missing bridge. Neither is allowed.

## Mechanical identity is not mechanism

Let revised macro data equal real-time data plus a revision component. A coefficient gap can always be
written as a function of covariances among returns, real-time observations and revisions. Predicting a
larger gap for factors with larger measured revision covariance is algebra, not an independent economic
restriction. It cannot elevate the paper to Level 3.

## Conclusion

No inspected literature supports a signed or ordered cross-factor prediction for the effect of
**statistical-agency** macro revisions. Candidate mechanisms support heterogeneous factor sensitivity to
macro states, surprises, or beliefs, but not heterogeneous sensitivity to later measurement revisions.
Kill condition K3 is therefore met.
