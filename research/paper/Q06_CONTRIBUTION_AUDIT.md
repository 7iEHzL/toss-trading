# Q06 Contribution Audit

## Scope and estimand

This audit asks whether Q06 contributes more than a new dependent variable to an established
macro-data-vintage critique. It does not redesign Q06 and authorizes no empirical work.

The estimand is held fixed:

> Given one fixed reconstruction of historical factor returns, how sensitive is a researcher's
> conditional asset-pricing inference to real-time versus ex-post revised macro information?

It is not a claim about what historical investors could have traded using today's reconstructed
factor history.

## Primary kill question

**Answer: yes.** A skeptical referee can reasonably characterize the current Q06 as an obvious
dependent-variable extension of Ghysels, Horan and Moench. Their econometric argument is explicitly
generic rather than Treasury-specific: final revised data can create spurious return predictability
when returns covary with information embedded only in later revisions. They then demonstrate the
problem using Treasury returns.

That objection is strengthened by two papers not safely dismissible as remote:

- Pierdzioch, Döpke and Hartmann already compare real-time and revised macro data for aggregate
  stock-return forecasting and find little difference in their German and unreported US exercises.
- Favero, Melone and Tamoni predict FF5 factor returns with macro trends and report real-time output
  variants. Adding a same-series revised-versus-real-time comparison is naturally a robustness table
  in their design, even though they do not report Q06's exact paired estimand.

Vincenz and Zeissler additionally use vintage series where available, or extra publication lags, in
allocating 21 cross-asset factors. This makes “macro information timing matters for factor analysis”
known practice, not a new mechanism.

## Contribution ladder

| Candidate claim | Level | Audit |
|---|---:|---|
| Repeat Ghysels with factor returns | 1 | Insufficient |
| Document descriptive differences across factor families | 2 | Insufficient |
| Test a preregistered economic ordering across factor families | 3 | Potentially sufficient, but no supported ordering was found |
| Identify a new measurement interaction | 4 | Not established |
| Establish a new economic mechanism | 5 | Not established |

The nearest defensible classification is **Level 2**. The exact table appears open; the independent
economic contribution does not.

## Concept discipline

| Concept | Source | Q06 role |
|---|---|---|
| Statistical-agency revision | Later official revisions to GDP, payrolls, IP, etc. | Treatment |
| Subjective expectation revision | SPF participants update forecasts | Adjacent mechanism only |
| Factor-return vintage | Historical factor files change after later database/method updates | Separate outcome-measurement dimension |

He, Su and Yu therefore cannot be cited as a direct statistical-vintage precedent. Akey, Robertson
and Simutin cannot be cited as a macro-vintage duplicate.

## Counterfactual novelty test

If Ghysels et al. replaced Treasury excess returns with FF factor returns, the paired coefficient and
forecast comparisons would follow directly. If they also split factors into families without a
pre-existing theoretical ordering, that would add descriptive heterogeneity but not identification.
The current Q06 offers no result that would be logically surprising under that counterfactual.

## Outcome discipline and null

Q06 does not require a profitable strategy. Its strongest form is a measurement/empirical-asset-
pricing audit. A null would mean that, under the fixed reconstruction and preregistered information
set, factor conditional inference is robust to macro vintage despite failures documented in bonds.
That is scientifically interpretable, but only **moderately** valuable because aggregate-equity and
real-time-factor studies already show that the magnitude need not transfer across return objects.

## Verdict basis

Kill conditions K2 and K3 are met: the strongest contribution is presently “bond/aggregate-equity
vintage sensitivity also examined for factors,” and no literature-supported ex-ante restriction was
found that predicts the cross-factor pattern of the macro-vintage coefficient gap. Exact-duplicate
absence does not cure those failures.
