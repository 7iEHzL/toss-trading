# Falsifiable Hypotheses — Draft for Pre-registration

These hypotheses are design drafts, not authorized empirical tests. Their separability is conditional
on the four-portfolio factorial construction in `ESTIMAND_AUDIT.md`; the original residual
decomposition cannot distinguish H2 from H3.

## H1 — Directional Component Stability

- Economic rationale: under a stable continuation mechanism, lagged directional signals should
  retain conditional predictive content after exposure is matched.
- Null: the signal coefficient is stable through time and equals across pre-specified subsamples.
- Alternative: the coefficient changes materially or becomes non-positive.
- Dependent variable: next-period excess return divided by ex-ante volatility.
- Explanatory variable: fixed lagged trend signal.
- Expected sign: positive under continuation.
- Primary test: panel interaction regression with a pre-specified period/state indicator and HAC
  or two-way clustered uncertainty; unknown-break test is a separate diagnostic.
- Rejection: family-wise adjusted p < 0.05 and economically material confidence interval excluding zero.

## H2 — Allocation Component Stability

- Economic rationale: inverse-volatility allocation adds value only if forecast risk and expected
  payoff relations remain stable after leverage is matched.
- Null: the matched-risk scaled-minus-unscaled component has stable mean and spanning coefficient.
- Alternative: its incremental value changes sign or magnitude.
- Dependent variable: scaled-minus-matched-unscaled component return.
- Explanatory variable: lagged risk forecast and pre-specified stability interaction.
- Expected sign: not imposed; a one-sided success test is inappropriate.
- Primary test: mean/spanning-coefficient stability with HAC confidence intervals.
- Rejection: adjusted p < 0.05 plus a material change relative to portfolio volatility.

## H3 — Signal × Allocation Interaction

- Economic rationale: volatility and correlation states may change how a directional position is
  converted into portfolio return beyond additive signal and allocation effects.
- Null: the interaction term is zero and stable.
- Alternative: the interaction is non-zero or changes across independently defined states.
- Dependent variable: next-period matched portfolio excess return.
- Explanatory variable: signal, allocation deviation from fixed reference, and their interaction.
- Expected sign: unsigned because the literature does not justify a directional prior.
- Primary test: panel interaction regression and block-bootstrap confidence interval.
- Rejection: adjusted two-sided p < 0.05 and sign stability across asset classes.
