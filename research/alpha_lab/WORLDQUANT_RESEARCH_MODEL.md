# WorldQuant Research-model Audit

Audit date: 2026-09-01. Public official sources were preferred. Logged-in BRAIN documentation was not
available, so unverified formulas and thresholds are marked `UNKNOWN`.

## Officially documented

WorldQuant defines an alpha as a mathematical model seeking to predict future price movements. The
2026 IQC uses historical market data and predefined operators to simulate equity positions whose weights
reflect expected next-period returns. Qualifying alphas proceed to out-of-sample scoring relative to other
participants. Team evaluation uses both quality and quantity; exact stage scoring may change. The official
guidelines also document a correlation test when alpha pools are combined, but not its public threshold.

Sources:

- [WorldQuant BRAIN IQC 2026](https://www.worldquant.com/brain/iqc/)
- [Official IQC 2026 Guidelines](https://www.worldquant.com/brain/iqc-guidelines/)
- [WorldQuant BRAIN overview](https://www.worldquant.com/brain/)

## Metric/status audit

| Concept | Public official status | Formula/rule status | Proposed local equivalent |
|---|---|---|---|
| Alpha expression | Predictive mathematical model using platform data/operators | Exact language/operator grammar requires platform docs | Versioned Python signal formula plus expression metadata |
| Universe | Equity positions and historical data are official; specific eligible universes vary | Current public universe definitions `UNKNOWN` | Frozen snapshot membership and eligibility rules |
| Sharpe | Common platform concept, but no current public official formula verified | `UNKNOWN` | Annualized mean net return / annualized volatility, convention recorded |
| Turnover | Public WorldQuant material recognizes turnover/cost linkage | BRAIN formula/threshold `UNKNOWN` | One-way traded notional / prior portfolio equity |
| Fitness | Mentioned in BRAIN community conventions | Current official formula `UNKNOWN` | No imitation; local multidimensional decision only |
| Returns | Performance is officially evaluated | Exact platform return convention `UNKNOWN` | Next-open, cost-adjusted portfolio return after Stage 1 signal evidence |
| Drawdown | Common evaluation concept | Official BRAIN definition/threshold `UNKNOWN` | Peak-to-trough portfolio equity drawdown |
| Neutralization | Official interviews mention group neutralization | Available modes/defaults `UNKNOWN` | Cross-sectional residualization/ranking by frozen group, if justified |
| Decay | Widely discussed platform setting | Current public definition/default `UNKNOWN` | Explicit lag/weighted signal transform, never assumed equivalent |
| Truncation | Widely discussed platform setting | Current public definition/threshold `UNKNOWN` | Explicit position cap in portfolio stage only |
| Coverage | Data availability is operationally required | Official metric/threshold `UNKNOWN` | eligible nonmissing signal count / eligible universe count |
| Correlation constraint | Official IQC guidelines confirm a correlation test | Metric, window and threshold `UNKNOWN` | signal-rank and realized-alpha-return correlation diagnostics |
| Submission requirements | Original work, qualifying OOS status, competition eligibility and relative scoring are documented | Detailed alpha qualification tests `UNKNOWN` | Not replicated locally |

Community formulas for Fitness or submission cutoffs are not treated as official and are not copied.

## Translation boundary

Local IC, rank IC, monotonicity, timestamp validation and multiple-testing governance have no guaranteed
one-to-one BRAIN analogue. A candidate may later be translated to a WorldQuant-style expression only
after semantic equivalence of data, operators, neutralization and timing is documented. Competition score
is not Alpha Lab scientific evidence.
