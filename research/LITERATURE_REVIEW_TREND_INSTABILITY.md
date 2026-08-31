# Literature Review — Trend Performance Instability and Risk Allocation

## Scope and Method

The review prioritizes peer-reviewed finance journals and established research papers. It
asks whether R5's temporal instability and component decomposition are already known, rather
than searching for rules that improve the backtest.

## Key Papers

### Moskowitz, Ooi and Pedersen (2012), Time Series Momentum

- Citation: [Journal of Financial Economics 104, 228–250](https://doi.org/10.1016/j.jfineco.2011.11.003).
- Research question: does an asset's own past return predict its future return?
- Dataset: 58 liquid futures/forwards across equity indices, bonds, currencies and commodities,
  primarily 1985–2009.
- Method: sign of past returns, especially 12-month returns; monthly portfolios; ex-ante EWMA
  volatility scaling.
- Main finding: positive continuation at 1–12 months and diversified TSMOM profitability.
- Mechanism: underreaction/delayed overreaction and possible hedger/speculator interaction.
- Limitations: futures long/short implementation and volatility scaling differ from R5 ETFs.
- Relation to R5: motivates the signal, but R5's later period does not reproduce stable payoff.

### Hurst, Ooi and Pedersen (2017), A Century of Evidence on Trend-Following

- Citation: [Journal of Portfolio Management 44, 15–29](https://doi.org/10.3905/jpm.2017.44.1.015).
- Question: is trend performance a recent statistical accident?
- Dataset: 67 markets across four asset classes, reconstructed back to 1880.
- Method: diversified monthly time-series momentum across long historical regimes.
- Finding: positive average performance across decades and many crisis environments.
- Mechanism: persistent trends and diversification across many independent markets.
- Limitations: reconstructed historical data, broad futures-like universe and shorting; not a
  nine-ETF long/cash test.
- R5 relation: R5's instability may reflect narrow universe/implementation rather than a direct
  contradiction of the century-scale evidence.

### Kim, Tse and Wald (2016), Time Series Momentum and Volatility Scaling

- Citation: [Journal of Financial Markets 30, 103–124](https://doi.org/10.1016/j.finmar.2016.05.003).
- Question: are TSMOM alphas attributable to the direction signal or volatility scaling?
- Dataset: 55 futures, 1985–2013.
- Method: compare scaled/unscaled TSMOM with scaled/unscaled buy-and-hold.
- Finding: large alphas are largely driven by volatility scaling; unscaled TSMOM does not
  significantly outperform unscaled buy-and-hold.
- Mechanism: leverage/risk allocation applied to assets with positive average returns.
- Limitations: portfolio-alpha comparison does not settle every conditional regime mechanism.
- R5 relation: directly makes a generic signal-versus-allocation decomposition `NOT NOVEL`.

### Goyal and Jegadeesh (2018), Cross-Sectional and Time-Series Tests

- Citation: [Review of Financial Studies 31, 1784–1824](https://doi.org/10.1093/rfs/hhx131).
- Question: why do time-series and cross-sectional momentum tests differ?
- Dataset/method: stocks and international asset classes; matched TS/CS return strategies.
- Finding: for stocks much of the difference is time-varying net long exposure; scaled CS
  outperforms similarly scaled TS across heterogeneous international asset classes.
- Mechanism: mean returns, net risky exposure and cross-sectional heterogeneity.
- Limitation: not designed around ETF long/cash allocation or structural-break timing.
- R5 relation: reinforces the need to separate directional alpha from net exposure.

### Huang, Li, Wang and Zhou (2020), Time Series Momentum: Is It There?

- Citation: [Journal of Financial Economics 135, 774–794](https://doi.org/10.1016/j.jfineco.2019.08.004).
- Question: is past-12-month predictability statistically reliable?
- Method: asset-level and pooled regressions with parametric/nonparametric bootstrap inference.
- Finding: asset-level and out-of-sample predictability is weak; pooled t-statistics are not
  reliable under their bootstrap; strategy profitability resembles a historical-mean rule.
- Mechanism: positive unconditional means rather than robust directional predictability.
- Limitation: disputed interpretation within a literature containing strong long-run evidence.
- R5 relation: consistent with R5's weak negative-signal hit rate and unstable direction payoff.

### Moreira and Muir (2017), Volatility-Managed Portfolios

- Citation: [Journal of Finance 72, 1611–1644](https://doi.org/10.1111/jofi.12513).
- Question: does reducing exposure when volatility is high improve factor portfolios?
- Dataset: major equity factors and currency carry.
- Method: inverse lagged realized-variance scaling and spanning regressions.
- Finding: positive alphas, Sharpe improvements and utility gains for many managed factors.
- Mechanism: volatility variation is not matched by proportional expected-return variation.
- Limitation: portfolio-level volatility timing differs from R5's cross-asset inverse-vol weights.
- R5 relation: provides the positive case for dynamic risk management, not a guarantee of stability.

### Cederburg, O'Doherty, Wang and Yan (2020), Performance of Volatility-Managed Portfolios

- Citation: [Journal of Financial Economics 138, 95–117](https://doi.org/10.1016/j.jfineco.2020.04.015).
- Question: do volatility-managed gains translate to implementable real-time portfolios?
- Dataset: 103 equity strategies.
- Method: direct Sharpe comparisons, real-time portfolio combinations and structural-break tests.
- Finding: managed portfolios do not systematically outperform; OOS combinations often
  underperform due to structural instability in spanning relations.
- Mechanism: unstable estimated relations and portfolio weights.
- Limitation: equity factors rather than multi-asset trend signals.
- R5 relation: makes broad risk-allocation instability `KNOWN/DEBATED`, but supports a sharper
  component-specific break question.

### Daniel and Moskowitz (2016), Momentum Crashes

- Citation: [Journal of Financial Economics 122, 221–247](https://doi.org/10.1016/j.jfineco.2015.12.002).
- Question: when and why does momentum crash?
- Dataset: long U.S. equity history plus international and other asset-class robustness.
- Method: momentum returns conditional on panic, volatility and rebound states.
- Finding: crashes follow market declines/high volatility and coincide with sharp rebounds.
- Mechanism: optionality-like payoff of past losers and changing market exposure.
- Limitation: primarily cross-sectional long-short momentum, not long/cash TSMOM.
- R5 relation: the missed-payoff result after negative signals is closely related, so a generic
  rebound explanation is not novel.

### Liu and Papailias (2023), Time Series Reversal in Trend-Following Strategies

- Citation: [European Financial Management](https://doi.org/10.1111/eufm.12349).
- Question: when does continuation reverse after trend signal formation?
- Dataset: 55 liquid futures, 1985–2015.
- Method: signal/subportfolio decomposition and continuation/reversal timing.
- Finding: statistically significant 12–24 month reversal, driven mainly by sell-signal losers.
- Mechanism: delayed overreaction/reversal.
- Limitation: futures long/short and longer post-formation horizon than R5's monthly payoff.
- R5 relation: R5's negative-signal assets subsequently rising is directionally similar and
  therefore `NOT NOVEL` by itself.

### Baltas and Kosowski (2020), Demystifying Time-Series Momentum

- Citation: [book chapter/established working paper](https://doi.org/10.2139/ssrn.2140091).
- Question: how do volatility estimation, trading rules, correlations and costs affect TSMOM?
- Method: implementation-component comparisons in futures.
- Finding: estimator and trend design can reduce turnover; correlation-aware allocation matters,
  especially post-2008.
- Limitation: extensive design choice creates specification degrees of freedom and is not a
  clean causal explanation of regime instability.
- R5 relation: confirms allocation/turnover implementation matters; it does not authorize tuning.

## Evidence Classification

### KNOWN

- Past-return continuation and diversified trend profitability have substantial historical support.
- Trend strategies can suffer in sharp reversals and rebound states.
- Volatility scaling/risk allocation can account for a material part of reported TSMOM performance.
- Trend implementation, universe breadth, correlation and cost matter.
- Volatility-managed relations may be structurally unstable out of sample.

### DEBATED

- Whether past 12-month returns provide reliable asset-level directional predictability after
  appropriate bootstrap/inference.
- Whether trend profits are behavioral underreaction, risk compensation, positive unconditional
  asset means, crisis convexity or an interaction of these mechanisms.
- How much value comes from directional signals versus volatility scaling after matching leverage.

### UNDERSTUDIED

- A unified, ex-ante component-level test of structural breaks in directional payoff and allocation
  value using identical assets, timing and leverage constraints.
- Whether the speed/path of a drawdown and rebound predicts which component—direction or
  allocation—fails, rather than merely whether total trend return is high or low.
- The implementation-domain gap between academic futures long/short TSMOM and accessible
  unlevered ETF long/cash overlays.

### NOT NOVEL

- Reporting that trend performance varies across periods.
- Reporting that sell-signal assets can reverse upward.
- Showing that volatility scaling changes TSMOM Sharpe ratios.
- Showing that trend can perform well in some crises and poorly during sharp rebounds.

### POTENTIAL CONTRIBUTION

The strongest potential contribution is not R5's two-period return contrast itself. It is a
pre-registered component-level structural-break study asking whether directional conditional
payoffs and allocation value change at the same time, and whether observable path geometry
explains the divergence. Publication-quality execution needs a much broader/longer dataset than
the current nine ETFs.
