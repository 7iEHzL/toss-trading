# R5 — New Strategy Research Program

## Status

`R5 COMPLETE — TEMPORAL/COMPONENT INSTABILITY; NO TRADING CANDIDATE; FINAL OOS SEALED`

R5는 frozen R1-002를 수정하거나 구제하는 단계가 아니다. R1–R4에서 확인한
concentration, regime dependence, turnover 및 data-quality 실패를 반영해 새로운 경제적
가설을 사전등록하는 독립 연구 프로그램이다.

## Primary Research Question

각 자산의 독립적인 중장기 추세로 방향 노출을 결정하고, 양의 추세인 자산 사이의
자본을 사전 고정된 위험기반 방식으로 배분하면, winner-take-all 상대 모멘텀보다
종목·기간 집중과 drawdown을 낮추면서 단순 위험배분 대비 일관된 위험조정 가치를
제공하는가?

## Approved Primary Candidate

`Long-or-cash multi-asset independent trend + unlevered risk-based allocation`

- 각 ETF는 다른 ETF와 순위를 비교하지 않고 자기 과거 가격으로만 활성/비활성을 정한다.
- 활성 ETF의 비중은 동일 명목비중이 아니라 과거 변동성에 반비례하도록 배분한다.
- 음의 추세 자산의 미사용 비중은 현금으로 둔다.
- 공매도와 레버리지는 첫 가설에서 사용하지 않는다.
- 포트폴리오 전체 volatility target은 첫 가설에서 사용하지 않는다. 이는 risk allocation과
  별개의 component이며 추가 자유도를 만들기 때문이다.

## Proposed Universe

R4A에서 성과와 무관한 category-first 규칙으로 2014-06-30에 동결한 다음 9개 ETF를
재사용한다.

`SPY, EFA, EEM, IEF, TLT, LQD, IYR, GLD, DBC`

이 universe는 주식, 국채 duration, 투자등급 신용, 상장 부동산, 금과 광범위 원자재를
포함한다. 모든 ETF는 2006-02-03까지 상장됐고 2013–2014 H1 audit에서 공통 SPY 거래일
coverage 100%를 통과했다. 다만 단일 국가 상장 ETF, USD 기준, 제한된 9개 proxy이며
현금수익률·FX hedge·완전한 global futures opportunity set을 나타내지는 않는다.

## Data-contamination Protocol

- Proposed development: `2007-03-01 through 2014-12-31`.
- Required warm-up: `2006-02-03 through 2006-12-31` 또는 선택된 canonical lookback을
  충족하는 더 긴 구간. DBC가 가장 늦게 시작한 ETF이므로 공통 universe의 실질적 하한이다.
- 이 기간의 실제 가격 coverage는 아직 다운로드·검증하지 않았다. R5-001 전 별도
  data-only gate에서 adjusted OHLC, common-calendar coverage, next-open availability,
  manifest hash와 2015 이후 행 0개를 확인해야 한다.
- 2013–2014 가격은 R4-000의 유동성·품질 audit에 사용됐지만 전략 성과는 계산되지 않았다.
  따라서 완전히 untouched인 기간은 아니며 이 제한을 명시한다.
- 2015–2022는 R1–R4에서 반복 관찰했으므로 clean validation/OOS로 부르지 않는다. 후보를
  고정한 뒤에도 secondary contaminated stress diagnostic으로만 사용할 수 있다.
- Final OOS 2023–2025는 double-confirmation seal을 유지한다.

The earlier `2007-01-01` proposal was corrected before any performance or pre-2013 price
inspection: DBC began on 2006-02-03, so a complete 12-month signal cannot exist at the
start of January 2007. March 2007 is the first conservative full evaluation month.

The data gate requires at least 95% common-calendar coverage and every series to begin by
2006-03-01. It does not require a row on the issuer inception date itself: DBC's first Yahoo
observation is the next trading day, 2006-02-06. An initial validator incorrectly required
`first_date <= 2006-02-03`; this implementation-only condition was removed without changing
the pre-registered coverage or warm-up requirements and before any strategy performance.

## Frozen Parameter Proposal

Option A 승인에 따라 다음 단일 specification을 R5-001 후보로 사전등록한다. 아직 성과를
실행하지 않았으며, 아래 ETF adaptation과 정량 판정 기준의 최종 확인 전까지 R5-001은
승인되지 않는다.

| Item | Proposed frozen value | Source/rationale |
|---|---|---|
| Trend signal | trailing 12-month adjusted total return `> 0` | Moskowitz, Ooi and Pedersen (2012)의 past 12-month sign |
| Direction | positive이면 long, 그 외 cash | ETF long-only operational constraint; short 금지 |
| Volatility | lagged daily-return EWMA, decay `60/61` | 문헌의 EWMA center-of-mass 60 trading days |
| Allocation | 활성 자산의 inverse-volatility를 합계 100%로 정규화 | unlevered risk allocation; portfolio vol target 금지 |
| Rebalance | 각 calendar month 마지막 거래일 close signal, 다음 거래일 open execution | 문헌의 monthly formation + backtest timing rule |
| Gross exposure | 최대 100% | leverage 금지 |
| Inactive budget | 현금, 수익률 0% | 첫 실험의 명시적 단순화 |
| Warm-up | 최소 12개월 및 EWMA 안정화 구간 | 가장 긴 signal requirement |

`12-month`는 구현 시 signal date 기준 직전 calendar-month-end부터의 adjusted total
return으로 정의한다. ETF 배당을 포함하되 T-bill 초과수익, futures roll return, short leg,
40% instrument volatility target은 재현하지 않는다. 따라서 이는 원 논문의 exact
replication이 아니라 문헌 기반의 사전 명시된 long-only ETF adaptation이다.

## Parameter Governance

성과를 보기 전에 다음 parameter가 필요하다.

| Parameter | Why needed | Allowed source |
|---|---|---|
| Trend horizon/definition | 각 자산의 활성 방향 결정 | canonical time-series-momentum literature |
| Volatility window/estimator | 활성 자산 사이 위험기반 비중 산출 | literature convention 또는 명시적 risk-estimation rationale |
| Rebalance frequency | 신호 갱신과 turnover 통제 | literature convention + operational constraint |
| Maximum gross exposure | unlevered 범위 보장 | operational risk constraint; proposed 100% |
| Cash treatment | 비활성 위험예산 보관 | explicit accounting rule |
| Warm-up | signal/volatility 추정 가능성 | 가장 긴 lookback 이상 |

첫 실험은 단일 canonical specification만 사용한다. 제한 robustness grid가 필요하면
R5-002 전에 별도 second opinion으로 범위와 판정 방식을 고정한다. Development 성과로
lookback, volatility window, threshold, leverage 또는 target volatility를 선택하지 않는다.

문헌 근거는 Moskowitz, Ooi and Pedersen (2012)의 time-series momentum과 Hurst, Ooi and
Pedersen (2017)의 장기 trend-following evidence를 우선한다. Risk allocation의 경제적
배경은 Asness, Frazzini and Pedersen (2012)을 참고하되, 해당 논문의 levered risk parity
성과를 이 ETF 구현의 성과로 간주하지 않는다. Volatility-managed portfolio는 별도
가설이며 첫 실험에 portfolio-level timing을 혼합하지 않는다.

## Baselines and Benchmarks

성과 조회 전에 다음 비교군을 고정한다.

1. `Equal-weight buy-and-hold`: 단순 경제적 diversification 비교.
2. `Unlevered inverse-volatility, no trend filter`: risk allocation 자체의 기여 분리.
3. `Equal-weight independent trend`: trend signal의 기여와 inverse-volatility weighting의
   기여 분리.
4. `SPY buy-and-hold`: 투자자의 단순 equity opportunity-cost benchmark.
5. R1-002/R4A 결과는 historical context일 뿐 R5의 최적화 baseline이 아니다.

## Pre-registered Decision Framework

### Primary metrics

- Sharpe and Calmar relative to both structural baselines
- MDD
- 10bps net benchmark excess
- subperiod stability

이는 R1–R4의 핵심 실패가 총수익보다 risk-adjusted benchmark value와 기간 안정성이었기
때문이다.

### Secondary metrics

- CAGR, Sortino and annual volatility
- turnover and 0/5/10/20bps cost robustness
- positive-subperiod ratio

### Diagnostic metrics

- asset-level absolute P&L contribution concentration
- maximum single-asset contribution and leave-one-asset-out sensitivity
- maximum subperiod contribution
- average number of active assets, cash allocation and holding duration
- trend overlay와 weighting overlay 각각의 incremental effect

### Proposed failure rule

R5-001은 10bps에서 다음 중 하나이면 `REJECT`한다.

1. candidate가 inverse-volatility/no-trend baseline보다 Sharpe와 Calmar 모두 높지 않다.
2. candidate가 equal-weight trend baseline보다 MDD 또는 concentration을 실질적으로
   개선하지 못하면서 Sharpe를 낮춘다.
3. SPY와 equal-weight buy-and-hold 양쪽에 대해 risk-adjusted value가 없고, 그 열위를
   명확한 MDD 개선으로도 보상하지 못한다.
4. 양의 성과 대부분이 단일 ETF 또는 단일 사전 고정 subperiod에 의존한다.
5. 10bps에서만 근소한 결과가 나타나고 20bps에서 경제적 결론이 뒤집히며 turnover로
   설명된다.

### Proposed quantitative adjudication

10bps primary 결과에서 다음을 모두 충족하면 `ACCEPT`한다.

1. inverse-volatility/no-trend baseline 대비 Sharpe `+0.10` 이상 및 Calmar `+0.05` 이상.
2. inverse-volatility/no-trend baseline 대비 CAGR excess가 양수.
3. equal-weight trend 대비 MDD가 3%p를 초과해 악화되지 않음.
4. 사전 고정 2년 구간 4개 중 최소 3개에서 total return이 양수.
5. 최대 단일 ETF absolute P&L contribution이 50% 미만.
6. 최대 단일 2년 구간 positive contribution이 전체 positive contribution의 60% 미만.
7. 20bps에서도 total return이 양수이며 inverse-volatility baseline 대비 Sharpe 우위의
   방향이 뒤집히지 않음.

1 또는 2를 실패하면 `REJECT`한다. 4–7 중 둘 이상 실패해도 `REJECT`한다. 그 밖에 primary
metric이 통과하지만 diagnostic 하나만 경계에서 실패하거나 P&L attribution이 완전히
reconcile되지 않으면 `INCONCLUSIVE`다. 이 기준은 R1–R4의 risk-adjusted, period/name
concentration과 cost failure를 직접 반영하며 성과 확인 후 완화하지 않는다.

## Transaction-cost Protocol

- Primary: one-way slippage 10bps, commission 0bps.
- Robustness: 0/5/10/20bps.
- Signal from close, execution at next available open.
- ETF spread, tax, market impact, cash yield와 FX는 별도 한계로 명시한다.

## Minimal Experiment Sequence

1. `R5-000`: family comparison, protocol and data feasibility design. Performance 0회.
2. `R5-001`: 승인된 단일 canonical specification의 simplest frozen implementation과
   structural baselines.
3. `R5-002`: 사전 승인된 cost/subperiod robustness만 수행. Parameter search는 별도 결정
   없이는 금지.
4. `R5-003`: candidate가 R5-001/002를 통과한 경우에만 asset/period dependency attribution.

## Authorization Boundary

Option A family는 승인됐다. R5-001은 위 exact ETF adaptation과 정량 threshold에 대한
사용자 확인 및 2006–2014 data-only gate 통과 전 실행하지 않는다. R4B 재개,
R1-002 수정, Final OOS 접근, broker API와 live order는 모두 범위 밖이다.

## R5-001 Outcome

The data-only gate passed with 9/9 assets, 99.9554% minimum common-calendar coverage and
no row after 2014-12-31. The frozen R5-001 run was `ACCEPT — DEVELOPMENT EVIDENCE ONLY`:
at 10bps CAGR 7.19%, Sharpe 0.905, Calmar 0.568 and MDD -12.66%. It passed every frozen
adjudication check but did not exceed SPY CAGR. This is not final candidate selection.

## R5-002 Outcome and Stop

The identical frozen rule was applied to the already-known 2015–2022 period strictly as a
researcher-contaminated stress diagnostic. At 10bps it returned -0.87%, Sharpe 0.037 and
Calmar -0.005 versus inverse-volatility/no-trend Sharpe 0.403 and Calmar 0.135. Only one of
four two-year blocks was positive, and the candidate turned negative between 5bps and 10bps.

R5-002 is `REJECT — STRONG PERIOD INSTABILITY`. Because this conflicts sharply with R5-001,
R5-003, adjacent parameter tests and Final OOS access are paused pending second opinion.

## R5-003 and Closure

The user authorized one bounded failure attribution under a publication-oriented objective.
R5-003 found weaker positive-signal payoff, larger missed rebound after negative signals and a
sign reversal in inverse-volatility allocation value. Transition false-rate did not increase, and
cost drag amplified but did not originate the later failure. R5 is closed without a trading
candidate. See `results/R5-003-bounded-failure-attribution.md` and `R5_COMPLETION_REPORT.md`.
