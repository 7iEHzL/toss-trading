# Metrics and Inference

## Primary empirical object

For signal `S(i,t)` and forward return `R(i,t+h)`, primary evidence is the time series of cross-sectional
association—not portfolio CAGR.

Recommended primary metrics:

- daily/periodic Pearson IC and Spearman rank IC;
- mean IC and rank IC;
- IC standard deviation and information ratio;
- positive-IC frequency;
- top-minus-bottom quantile forward-return spread and monotonicity.

Secondary metrics:

- signal decay across preregistered horizons;
- coverage and missingness by date/security;
- signal persistence and turnover;
- long-short spread after a frozen cost model;
- security, sector and time-period concentration;
- benchmark/factor exposures and candidate redundancy.

## Inference plan

- Aggregate cross-sectional IC through time; do not treat security-date rows as independent.
- HAC/Newey–West is appropriate when horizon overlap/serial dependence is material, with lag fixed from
  the holding horizon before results.
- Block bootstrap is a robustness tool for temporal dependence and non-normality; block construction is
  preregistered.
- Cross-sectional dependence motivates date-level statistics and, where needed, clustered/two-way
  methods rather than naive pooled t-tests.
- Quantile portfolios require frozen breakpoints, weighting, rebalance timing and delisting treatment.

Advanced inference is not implemented in v1 design. Its location is the future common evaluation engine,
not individual alpha scripts.
