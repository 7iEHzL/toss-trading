# Publication Feasibility Report

## Proposed Study

- Proposed title: **When Trend Components Break: Directional Predictability, Dynamic Risk Allocation, and Their Interaction**
- Primary field: empirical asset pricing
- Secondary field: quantitative finance / portfolio choice
- Research question: when a fixed trend strategy changes through time, which statistically
  identifiable change belongs to directional payoff, dynamic allocation, or their interaction
  after implementation dimensions are matched?
- Why it matters: the three explanations imply different asset-pricing interpretations and
  different expectations for real-time robustness. Total strategy returns cannot distinguish them.

## Literature Position

- Consensus: volatility scaling, net exposure, correlation, reversals and implementation choices
  materially influence measured momentum/trend performance.
- Disagreement: the reliability and economic source of directional time-series predictability,
  and whether dynamic risk scaling adds stable OOS value after matched exposure.
- Closest papers:
  1. Kim, Tse & Wald (2016) — scaled versus unscaled TSMOM.
  2. Huang et al. (2020) — weak directional predictability and bootstrap inference.
  3. Cederburg et al. (2020) — structural instability of volatility management.
  4. Goyal & Jegadeesh (2018) — exposure-matched TS/CS decomposition.
  5. Liu & Papailias (2023) — sell-signal reversal.

## Decision

`MODIFY — HIGH CLOSEST-PAPER THREAT; NO EMPIRICAL EXECUTION AUTHORIZED`

## Novelty Attack

### A. Has direction versus scaling already been decomposed?

Yes, substantially. Kim, Tse and Wald directly compare scaled/unscaled TSMOM and buy-and-hold;
Goyal and Jegadeesh isolate net exposure; Huang et al. challenge directional predictability.

### B. Is every implementation dimension held identical?

Not completely across the literature. Individual papers match many dimensions, but no reviewed
paper was verified as jointly fixing universe, sample, leverage, risk, timing and costs while testing
both component stability and their interaction.

### C. Are structural changes formally tested?

Yes for volatility-managed portfolios generally (Cederburg et al.) and return-prediction models,
but direct joint TSMOM component-break evidence appears less complete. This is a narrow gap, not
a broad untouched field.

### D. Is signal × allocation interaction directly estimated?

Nearby work studies volatility scaling, correlation regimes and momentum states. A fully matched,
pre-registered joint interaction test was not verified in this review, but unpublished or recent work
could eliminate the gap.

### E. Exact defensible difference

The viable difference is a single matched design that estimates whether directional conditional
payoff and allocation value change concurrently, with explicit interaction, leverage matching,
costs and controlled break inference. Merely showing performance decay or comparing scaled and
unscaled returns is not novel.

## Novelty

`WEAK` after the adversarial 2026 search. Sepp and Lucic provide an exact trend-system P&L
decomposition, while Kurth et al. directly study post-2009 decay in a broad futures panel. A narrow
factorial interaction/stability design remains conceivable, but it does not yet supply new economic
information beyond the combined literature.

## Proposed Contribution

Prior research separately documents that volatility scaling can dominate reported TSMOM alpha
and that volatility-managed relations can be unstable. It remains incompletely established whether
directional payoff and allocation value change jointly under the same assets, dates, leverage,
timing and costs. The proposed study supplies a pre-registered matched-risk decomposition and
formal component-stability tests; it does not claim that the decomposition is causal.

- Empirical: synchronized evidence on component stability in a broad multi-asset panel.
- Methodological: explicit separation of an accounting identity, matched counterfactuals and
  econometric estimands.
- Economic: distinguish fading continuation from unstable risk transformation.
- Practical: conditional on results, clarify which component makes historical trend estimates
  fragile. No practical benefit is asserted before testing.

## Design Summary

- Hypotheses: H1 directional coefficient stability; H2 scaled-minus-unscaled allocation stability;
  H3 signal-allocation interaction stability.
- Identification: fixed signal and reference weights, matched gross exposure/volatility, explicit
  cost term, panel estimates and externally defined states. Association is not a causal regime effect.
- Main tests: HAC/two-way clustered interaction regressions, block-bootstrap confidence intervals,
  matched-risk spanning tests, multiplicity-controlled component tests and an unknown-break
  diagnostic that cannot define the favored sample.
- Required data: 25–30 years minimum, preferably 40+, broad international futures, raw contracts
  or fully documented rolls, settlement returns, multipliers, FX, financing and historical costs.
- Free-data feasibility: adequate for pilot code or a narrower Tier C ETF study; inadequate for a
  global managed-futures conclusion.
- University/institutional opportunity: Datastream, Bloomberg, WRDS entitlements and exchange
  archives could support Tier B. Availability and publication/export rights require user confirmation.

## Threats to Validity

1. Literature overlap may be greater than discoverable from accessible abstracts.
2. Continuous-futures and roll conventions can manufacture component differences.
3. Break-date and state-variable selection can become data mining.
4. Common shocks, few asset classes and overlapping signals reduce effective sample size.
5. Leverage, financing and cost matching may remain imperfect.
6. R5 pilot periods are researcher-contaminated and cannot define the publication split.
7. Public ETF data create short-history and implementation-domain limitations.

## Expected Publication Tier

`C currently; B conditionally`

Tier C is realistic if the design is executed transparently with public data and narrow claims.
Tier B would require institutional multi-asset futures data, formal inference, a new testable economic
restriction, a verified literature gap
and independent econometric review. Tier A is not a realistic current expectation because neither
novelty nor identification is yet strong enough.

## Recommendation

Do not run a backtest. First obtain a second opinion on whether the factorial interaction is more than
measurement hygiene and determine whether university/institutional futures data are accessible. If
neither survives, pivot to a Tier C
replication/measurement paper rather than claim global structural instability.

## If Modified Study Proceeds

- Provisional architecture: see `PAPER_PLAN.md`.
- Pre-registration items: see `PREREGISTRATION.md`.
- Next implementation step: **not a backtest**. Confirm institutional data access and obtain a
  second opinion on whether the narrowed joint-stability contribution is sufficiently distinct.

## Alternative Questions if the Gap Fails

1. How much of the apparent gap between academic futures trend and accessible ETF long/cash trend
   is attributable to short legs, leverage, roll yield, financing and trading costs under matched risk?
2. Does pre-defined drawdown duration and rebound speed explain trend component failure better than
   binary crisis labels across independently dated events?

## Safety State

- Final OOS 2023–2025: `SEALED`
- New strategy optimization: `NO`
- Parameter tuning: `NO`
- Performance backtest: `NO`
- Broker/live-order calls: `0`
