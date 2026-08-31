# Q06 Core-paper Reassessment

| Paper | Exact research question | Dependent variable | Macro variable | RT used? | Revised used? | Direct pair? | Revision type | Factor vintage? | Conditional factor inference? | Factor allocation? | Mechanism / estimand | Genuine overlap | Not overlap | Could Q06 be one robustness table? |
|---|---|---|---|---:|---:|---:|---|---:|---:|---:|---|---|---|---|
| Ghysels, Horan & Moench, *Forecasting through the Rear-view Mirror* | How publication lags and later official revisions alter macro-based Treasury-return predictability | Treasury excess returns | 68-series macro panel/PCA; payroll exercise | Yes | Yes | Yes | Statistical-agency | No | No | No | Decompose final macro data into real-time, publication-lag and revision components; quantify infeasible predictability | Same treatment, information-set problem, paired logic and generic predictive-regression theory | Bond outcomes, yield controls and bond announcement response | **Yes.** Substitute fixed factor returns for Treasury returns and repeat their vintage decomposition |
| Vincenz & Zeissler, *Time-Varying Factor Allocation* | Can macro and market predictors improve allocation across 21 cross-asset factors? | 21 equity, commodity, fixed-income and FX factor returns | CFNAI/ADS, inflation, rates, money and other predictors | Partly | Not as paired treatment | No | Statistical vintage handled operationally | No | Yes | Yes | Predictor-conditioned factor allocation; use vintages where available or an extra lag | Macro-conditioned factor inference; explicit concern with delays/revisions; broad factor universe | No controlled MacroVintage contrast; several series not perfectly real-time | **Probably.** A paired vintage sensitivity appendix could be added without changing the paper's allocation question |
| Akey, Robertson & Simutin, *Noisy Factors?* | Do retroactive FF factor-file changes alter downstream finance inference? | FF factors, anomaly alphas, fund alphas, GRS tests | None | No | No | Factor-vintage pair | Factor-return/database/method revision | Yes | Downstream inference, not macro-conditional | No | Hold sample fixed, vary FactorVintage; measure inference instability | Establishes that Q06's outcome reconstruction is itself vintage-dependent | Does not vary macro information or study statistical-agency revisions | **No** as a literal table: it would introduce a different treatment and literature. It instead bounds Q06's interpretation |
| He, Su & Yu, *Macroeconomic Perceptions, Financial Constraints, and Anomalies* | Do revisions in subjective productivity expectations predict heterogeneous anomaly returns through financing constraints and overreaction? | Anomaly and constrained-minus-unconstrained returns | SPF one-quarter-ahead IP growth forecast revisions; initial-release realized IP as control | Yes | No final-data treatment | No | Subjective expectation | No | Yes | Yes | Expectation revisions affect investment/financing and mispricing more for constrained firms | Provides an ex-ante cross-anomaly ordering for **belief revisions** and shows factor heterogeneity can have mechanism | Not statistical-agency revision; no RT-versus-final comparison; different causal object | **No** as Q06's exact table: replacing beliefs with official revisions breaks the mechanism. A macro-vintage sensitivity check could be ancillary only |

## Paper-specific conclusions

### Ghysels, Horan and Moench

The paper's theory says the revision problem applies beyond bonds. Its bond application finds that a
substantial fraction of predictive content comes from future, including benchmark, revisions and that
even survey-observable information does not explain all of it. Q06 inherits their method, not a new
identification strategy.

### Vincenz and Zeissler

The paper explicitly recognizes delayed publication and frequent revision, constructs vintage series
where available, and otherwise adds a month of lag. It also cautions that pre-inception CFNAI/ADS
histories are not perfectly real time. It is not a paired-vintage paper, but it makes the proposed factor
application look incremental.

### Akey, Robertson and Simutin

The published Review of Finance study varies only FactorVintage while holding the sample fixed. That
is orthogonal to Q06's intended MacroVintage treatment. Its implication is disclosure and bounded
interpretation, not automatic requirement of a two-dimensional design.

### He, Su and Yu

Their revision is an SPF belief update available during the quarter, not an official agency rewriting
of realized history. Their financing-constraint mechanism cannot be transferred to agency revisions
without a new bridge. Calling it direct Q06 overlap would conflate economically different concepts.

## Additional near neighbors exposed by the audit

- Pierdzioch, Döpke & Hartmann (2008) directly compare real-time and revised macro information in
  aggregate stock forecasting. This removes any claim that equity application itself is new.
- Favero, Melone & Tamoni (2022 working paper) connect FF5 factor prices and macro trends, then show
  predictability with real-time output and recursive real-time estimation. Q06's exact pair is absent,
  but it is plausibly one additional sensitivity table.
