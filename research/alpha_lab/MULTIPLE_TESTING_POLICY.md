# Multiple-testing and Parameter-governance Policy

## Ledger rule

Every tested alpha, failed data attempt and parameter variant is counted in `ALPHA_CATALOG.csv`. IDs are
never reused or deleted. Reports disclose total tests globally, by family, lineage, period and universe.

## Parameters

- **Economic parameter:** encodes the hypothesis, such as a literature-motivated horizon.
- **Implementation parameter:** calendar, lag, ranking and missing-value mechanics required to calculate it.
- **Optimization parameter:** a value varied to improve observed results.

Variants use lineage IDs such as `A010-v01` and consume the same family research budget. A variant grid
must be frozen as a finite set before any result in that grid is viewed. Unplanned neighboring searches
start a new explicitly contaminated optimization phase.

## Adjustment tools

- Benjamini–Hochberg FDR: appropriate for a preregistered family/cohort of comparable hypotheses and
  valid p-values; not a cure for hidden tests or dependent arbitrary specifications.
- Deflated Sharpe Ratio: relevant in a later portfolio stage when many strategies/variants were tried and
  return non-normality and selection bias matter; not the primary IC discovery statistic.
- Probability of Backtest Overfitting: relevant to an explicit multi-configuration selection exercise with
  enough configurations/time observations; inappropriate for a single alpha or tiny search set.
- Family-wise experiment counts and unadjusted plus adjusted inference are always reported.

No method legitimizes an undocumented search. Raw effects, uncertainty, economic magnitude and all
failed hypotheses remain visible.
