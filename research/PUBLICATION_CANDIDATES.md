# Publication-oriented Research Candidates after R5

## Candidate 1 — Component-level Structural Instability

- Research question: when TSMOM performance changes across time, does instability originate in
  directional predictability, volatility/risk allocation, or their interaction?
- Why it matters: alpha interpretation and real-time portfolio construction imply different
  mechanisms and different falsification tests.
- Literature known: Kim et al. separate scaling from signal in aggregate; Huang et al. question
  directional predictability; Cederburg et al. document instability in volatility management.
- Gap: unified ex-ante break analysis of both components under matched assets, timing, leverage and costs.
- Potential contribution: locate and compare break timing rather than report another strategy return.
- Required data: long monthly/daily futures or index histories across many markets, risk-free returns,
  contract rolls and implementable costs. Current ETFs can pilot code but cannot support the main claim.
- Identification: frozen signal and allocation; component returns; Bai–Perron or pre-specified split
  tests; interactions with independently defined state variables.
- Main empirical test: HAC/two-way clustered regression of next return on signal, plus spanning
  comparison of scaled/unscaled component returns across breaks.
- Falsification: no stable break difference between components, or results vanish under matched
  leverage and block bootstrap.
- Main risk: break dates and regime variables can become data-mined.
- Free-data feasibility: LOW–MEDIUM for publication, HIGH for pilot.
- Publication potential: MEDIUM–HIGH with credible broad data; LOW with current R5 alone.

## Candidate 2 — Drawdown Path Geometry and Trend Failure

- Research question: is trend payoff determined more by drawdown duration/rebound speed than by
  a binary crisis label?
- Why it matters: “crisis alpha” is unreliable if fast reversals systematically defeat lagged signals.
- Literature known: trend often helps in prolonged crises; momentum crashes occur during rebounds.
- Gap: pre-specified path geometry linked separately to positive- and negative-signal payoff and
  allocation effects across asset classes.
- Contribution: replace ex-post crisis labels with measurable duration, monotonicity and rebound-speed tests.
- Data: many international futures/index markets and independently dated crisis events.
- Identification: event-time panels around externally dated drawdowns; interactions fixed before testing.
- Main test: local projections/event study with asset and event fixed effects, time-clustered/HAC errors.
- Falsification: path interactions have no consistent sign across held-out events/assets.
- Main risk: few independent crises and endogenous event definitions.
- Free-data feasibility: MEDIUM for exploratory indices; LOW for publication-quality futures.
- Publication potential: MEDIUM, but novelty overlaps momentum-crash/crisis-alpha literature.

## Candidate 3 — Futures Evidence versus ETF Long/Cash Implementability

- Research question: which documented TSMOM findings survive when shorting, leverage, futures roll
  exposure and interest on cash are replaced by an unlevered ETF long/cash implementation?
- Why it matters: academic and retail/institutional-accessible strategies are economically different.
- Literature known: most canonical evidence uses diversified futures long/short and volatility targets.
- Gap: matched-underlying comparison holding signal dates and risk budgets constant.
- Contribution: identify whether performance gaps arise from short legs, leverage, roll yield, cash
  return, cost or ETF tracking.
- Data: matched ETF/index/futures histories, total returns, roll series, T-bill returns and costs.
- Identification: synchronized matched pairs and sequential component removal; no optimized parameters.
- Main test: paired return differences with block bootstrap and spanning regressions.
- Falsification: ETF/futures difference is economically negligible after matched exposure and costs.
- Main risk: short common history and imperfect exposure matching.
- Free-data feasibility: LOW–MEDIUM.
- Publication potential: MEDIUM as an implementation paper, lower for top empirical asset-pricing outlets.

## Recommendation

Candidate 1 is the provisional priority. It most directly integrates the genuine literature debate and
R5 evidence, has a falsifiable decomposition, and avoids pretending that a nine-ETF return contrast is
novel. Candidate 2 is a possible mechanism extension; Candidate 3 is more feasible/practical but has a
lower theoretical contribution.

No candidate is authorized for empirical execution. Dataset access, identification and primary tests
require a separate second-opinion decision. Final OOS remains SEALED.
