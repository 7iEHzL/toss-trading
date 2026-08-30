# R1 Baseline Strategy Research Plan

## Status

`R1 COMPLETE — R1-002 FROZEN DEVELOPMENT CANDIDATE`

Second opinion 결정에 따라 Cross-sectional Momentum Rotation을 primary baseline으로 확정했다. 2015–2022 development snapshot으로 R1-001부터 R1-003까지 평가했으며 R1-002를 development candidate로 유지한다. Routine research decision은 `RESEARCH_PRINCIPLES.md`의 범위 안에서 자율 수행하며 2023–2025 final OOS는 미다운로드·미조회 상태다.

## Research Question

향후 factor 연구의 비교 기준으로 사용할 수 있는 가장 단순하고 해석 가능한 기존 전략은 무엇인가?

## Hypothesis

- 변경하려는 내용: 기존 전략의 alpha나 parameter는 변경하지 않고 하나를 R1 baseline으로 지정한다.
- 근거: baseline은 복잡한 성과 극대화 전략보다 factor의 incremental contribution을 분리할 수 있는 단순한 전략이어야 한다.
- Baseline: Cross-sectional Momentum Rotation. Primary universe에서는 SPXL을 제외하며 SPXL 포함은 별도 robustness test로만 실행한다.
- 성공 기준: 사전 등록된 OOS에서 benchmark 대비 양의 excess return뿐 아니라 Sharpe/Sortino/Calmar가 악화되지 않고, 비용 적용 후에도 방향성이 유지되며, 특정 단일 자산에만 결과가 의존하지 않는다.
- 실패 기준: OOS excess return이 음수이거나, 성과가 한 종목·한 구간에 집중되거나, 비용 및 인접 조건에서 risk-adjusted 성과가 붕괴한다.

## Candidate Comparison

| 후보 | 장점 | 핵심 약점 | R1 적합성 |
|---|---|---|---|
| 단일 종목 MA/RSI/Breakout/Momentum | 단순하고 해석 가능 | 한 종목 결과이며 cross-sectional factor baseline이 아님 | 진단용 control |
| Cross-sectional Momentum Rotation | 가격 데이터만 사용, factor가 하나라 attribution이 명확 | Top 1 집중, 항상 risk-on, 사후 universe 가능성. 기존 구현의 SPXL은 primary에서 제외 | Primary baseline |
| Multifactor v1 | composite 구조가 단순 | 정적 ROE/PBR 편향, Top 1, 방어 필터 없음 | 제외 |
| Multifactor v2 | Top 2, absolute momentum과 장기 MA로 현금화 가능 | 정적 ROE/PBR 편향, 여러 component가 이미 결합됨 | 후보 B |
| Multifactor v3 | 추가 trend/RSI 필터 | baseline으로는 component가 많고 과적합 위험 증가 | 후속 candidate |
| Multifactor v4 | ATR stop 포함 | stop 효과와 factor 효과가 섞임 | 후속 robustness |
| Multifactor v4.1 | inverse-volatility allocation | factor와 sizing 효과가 섞임 | 후속 allocation 연구 |

## Pre-registered Experimental Design

아래 값은 2026-08-28 second opinion decision으로 확정했다. Final OOS를 본 뒤 변경하지 않는다.

- Development/walk-forward: 2015-01-01 ~ 2022-12-31
- Final untouched OOS: 2023-01-01 ~ 2025-12-31. 연구 iteration 중 반복 조회 금지
- Primary universe: AMD, TSLA, AMZN, AAPL
- Robustness universe: primary universe + SPXL
- Universe는 ex-post 선정되었으며 selection/survivorship bias를 모든 결과에 표시
- Primary benchmark: SPY adjusted buy-and-hold
- Secondary benchmark: universe equal-weight buy-and-hold
- Currency: USD 단일 통화
- Initial cash: USD 100,000
- Cost assumption: commission 0 bps, one-way slippage 10 bps
- Cost robustness: one-way slippage 0/5/10/20 bps
- Metrics: cumulative return, CAGR, annual volatility, MDD, Sharpe, Sortino, Calmar, turnover, trades, benchmark return, excess return
- Parameter search: R1에서는 없음. 21/63/126 momentum, 동일 factor weight, 5거래일 rebalance를 그대로 사용
- Decision: total return 단독이 아니라 OOS risk-adjusted 성과, 비용 민감도 및 집중도를 함께 평가

## Execution Gate

다음 조건 전에는 R1 성과 실험을 실행하지 않는다.

1. adjusted-price와 SPY를 포함한 로컬 `DataSnapshot` 확보
2. snapshot provenance와 날짜 범위 검증
3. development-only runner로 R1-001 실행
4. final OOS는 candidate와 판정 규칙이 고정될 때까지 봉인

## Planned First Experiment

- ID: `R1-001`
- 단일 질문: 선택된 baseline의 기존 parameter 성과가 OOS와 거래비용 적용 후에도 유지되는가?
- 변경: alpha/parameter 변경 없음
- 결과 판정: `ACCEPT`, `REJECT`, `INCONCLUSIVE`

## Candidate Preservation

Multifactor v2는 baseline에서 제외하지만 후속 candidate strategy로 보존한다. R1 baseline 평가가 끝나기 전에는 v2 parameter를 조정하지 않는다.

## R1-002 Pre-registration — 126-day Absolute Momentum Risk-off

- Research question: 항상 risk-on인 baseline의 downside가 선택된 winner의 기존 126일 절대 momentum을 사용한 cash filter로 개선되는가?
- Hypothesis: winner의 126일 absolute momentum이 0 이하일 때 다음 거래일 시가부터 현금을 보유하면 약세 국면 노출과 MDD를 줄일 수 있다.
- Baseline: R1-001 primary baseline을 변경하지 않고 그대로 비교한다.
- Single change: 선택된 winner의 126일 absolute momentum `<= 0`이면 target을 cash로 설정한다.
- Unchanged: universe, 21/63/126 relative momentum, 동일 factor weight, Top 1, 5거래일 rebalance, next-open execution, benchmark, 비용 조건.
- Primary success criteria: MDD, Sharpe, Sortino, Calmar 및 2021–2022 downside가 baseline보다 개선.
- Guardrail: total return 증가만으로 ACCEPT하지 않는다.
- Cost robustness: 0/5/10/20bps.
- Additional diagnostic: 동일 규칙에서 TSLA 제외. Baseline 변경이나 parameter tuning에 사용하지 않는다.
- Final OOS: 2023–2025 미다운로드·미조회 상태 유지.

## R1-003 Pre-registration — Top 2 Equal-weight Diversification

- Research question: R1-002의 단일 종목 집중을 Top 2 동일가중으로 완화하면 momentum premium의 상당 부분을 보존하면서 MDD와 손익 집중도를 낮출 수 있는가?
- Hypothesis: 상대 모멘텀 상위 두 종목에 각각 50% 목표비중을 부여하면 특정 종목 경로에 대한 의존도가 감소하여 Sharpe와 Calmar가 개선될 수 있다.
- Baseline: R1-002 126-day absolute-momentum risk-off candidate.
- Single change: selection을 Top 1에서 Top 2 equal-weight로 변경한다.
- Risk-off rule: 각 Top 2 후보에 기존 126-day absolute momentum 조건을 독립 적용한다. 양수인 후보에는 각각 50%를 배분하고, 조건을 통과하지 못한 후보의 50% 몫은 현금으로 유지한다.
- Unchanged: universe, 21/63/126 relative momentum, factor weights, 5거래일 rebalance, next-open execution, benchmark, 0/5/10/20bps 비용 조건.
- No search: Top N 또는 weight 조합을 추가 탐색하지 않으며 실패 시 Top 3 등으로 즉시 재튜닝하지 않는다.
- Success criteria: Sharpe와 Calmar 개선, MDD 감소, 거래원장 기준 single-name realized-P&L concentration 감소, CAGR 및 benchmark excess return의 합리적 보존을 함께 평가한다. 단순 MDD 감소만으로 ACCEPT하지 않는다.
- Concentration disclosure: 종목별 realized P&L, 최대 절대 realized-P&L share와 지배 종목을 기록한다. 이는 완전한 portfolio return attribution이 아니라 거래원장 기반 진단이다.
- Final OOS: 2023–2025는 미다운로드·미조회 상태를 유지한다.

### R1-003 Decision

`REJECT`. Top 2는 MDD와 변동성을 낮췄지만 10bps에서 Calmar와 Sortino가 하락했고, 거래원장 기준 최대 단일 종목 절대 실현손익 비중도 71.49%에서 80.03%로 상승했다. CAGR은 63.75%에서 44.74%로 감소했다. 사전 등록한 공동 성공 기준을 충족하지 못했으므로 R1-002를 development candidate로 유지하며 Top 3 또는 다른 가중치를 탐색하지 않는다.

## R1-004 Pre-registration — Remove Short-horizon Momentum Component

- Research question: 21/63/126-day composite가 최근 21일 수익을 세 구간에 중복 반영하는 구조에서 21-day 항을 제거하면 단기 움직임 민감도와 종목 손익 집중을 줄이면서 중기 momentum premium을 보존할 수 있는가?
- Hypothesis: R1-002의 risk-off와 execution은 유지하고 relative score에서 21-day 항만 제거하여 63/126-day momentum을 동일가중하면 turnover 또는 concentration이 낮아지고 risk-adjusted 성과의 시간 구간 일관성이 개선될 수 있다.
- Baseline: R1-002 126-day absolute-momentum risk-off candidate.
- Single change: relative momentum weight를 21/63/126 = 1/1/1에서 0/1/1로 변경한다.
- Unchanged: universe, 63/126 lookback, 126-day absolute-momentum risk-off, Top 1, 5거래일 rebalance, next-open execution, benchmark와 비용 조건.
- No search: 다른 lookback, skip period 또는 weight 조합을 탐색하지 않는다.
- Success criteria: 10bps primary에서 Sharpe와 Calmar가 악화되지 않고, turnover 또는 최대 single-name absolute realized-P&L share가 개선되며, CAGR과 두 benchmark 대비 excess return의 상당 부분을 보존한다. 0/5/10/20bps와 시간 구간에서 방향이 심하게 충돌하면 INCONCLUSIVE로 판정한다.
- Failure criteria: risk-adjusted metric과 concentration/turnover가 함께 개선되지 않거나 momentum premium 희생이 과도하면 REJECT한다.
- Final OOS: 2023–2025 미다운로드·미조회 상태 유지.

### R1-004 Decision

`INCONCLUSIVE`. 전체 development와 0/5/10/20bps에서는 Sharpe, Sortino, Calmar, CAGR과 turnover가 개선됐지만 2021–2022 downside 및 TSLA realized-P&L concentration은 악화됐다. 시간 구간상 강한 방향 충돌이 있으므로 R1-004를 채택하거나 폐기하지 않고 연구 기록으로 보존한다. R1-002를 development candidate로 유지하며 인접 weight/lookback은 탐색하지 않는다.

## Bounded Batch Pre-registration — R1-005 to R1-007

2026-08-30 second opinion으로 Option A를 채택했다. 아래 세 가설을 결과 조회 전에 함께 고정하고 모두 실행한 뒤 development 탐색 batch를 종료한다. 각 실험은 R1-002에 독립 적용하며 결합하지 않는다.

### Common Decision Rule

- Primary comparison: R1-002, 10bps.
- ACCEPT: Sharpe/Sortino/Calmar 중 최소 2개 개선, 어느 지표도 0.05 초과 악화 없음, MDD 악화 3%p 이내, CAGR baseline의 80% 이상, SPY·equal-weight 대비 양의 excess return, turnover 증가 20% 이내.
- REJECT: 위 필수 조건을 충족하지 못하고 증거 방향이 명확함.
- INCONCLUSIVE: 전체기간, 비용 조건 또는 시간 구간의 강한 증거가 충돌함.
- Diagnostics: 0/5/10/20bps, 2년 구간, 거래원장 realized-P&L concentration.
- Stop rule: ACCEPT 발생 여부와 관계없이 R1-005~R1-007을 모두 평가한 후 이 batch를 종료한다. 인접 parameter를 추가 탐색하지 않는다.
- Final OOS: 2023–2025 미다운로드·미조회 상태 유지.

### R1-005 — Volatility-adjusted Relative Momentum

- Hypothesis: 기존 21/63/126 composite score를 각 종목의 trailing 63-day daily volatility로 나누면 변동성이 큰 단일 종목의 score 지배를 완화하고 risk-adjusted 성과와 concentration을 개선할 수 있다.
- Single change: selection score = 기존 composite / trailing 63-day volatility.
- Fixed: volatility lookback 63 trading days. Annualization은 ranking에 공통 상수이므로 적용하지 않는다.
- No search: 다른 volatility window, winsorization 또는 scaling 방식을 탐색하지 않는다.

### R1-006 — Cross-sectional Breadth Gate

- Hypothesis: universe 네 종목 중 126-day absolute momentum이 양수인 종목이 절반 미만이면 cash를 보유하면 광범위한 약세 국면의 downside를 줄일 수 있다.
- Single change: positive breadth가 2/4 미만이면 전체 target을 cash로 설정한다.
- Fixed: 기존 126-day lookback과 threshold 2. Winner의 기존 R1-002 risk-off도 유지한다.
- No search: threshold 또는 lookback을 탐색하지 않는다.

### R1-007 — SPY Market-regime Gate

- Hypothesis: winner가 양의 absolute momentum이어도 SPY의 126-day return이 0 이하인 시장 약세 국면에는 cash를 보유하면 systematic downside를 줄일 수 있다.
- Single change: SPY 126-day absolute momentum `<= 0`이면 전체 target을 cash로 설정한다.
- Fixed: existing snapshot의 SPY와 기존 126-day lookback.
- No search: 다른 benchmark, moving average 또는 lookback을 탐색하지 않는다.

### Bounded Batch Decision

- R1-005: `REJECT`. Concentration과 2021–2022 downside는 개선됐지만 10bps Sharpe/Sortino/Calmar가 모두 악화되고 CAGR 보존율이 76.46%로 80% 기준에 미달했다.
- R1-006: `REJECT`. Turnover와 2021–2022 downside는 개선됐지만 Sharpe/Sortino/Calmar가 모두 악화되고 TSLA realized-P&L concentration이 86.13%로 상승했다.
- R1-007: `REJECT`. MDD, concentration과 일부 downside는 개선됐지만 Sharpe/Sortino/Calmar가 모두 악화되어 공통 필수 기준을 충족하지 못했다.
- Stop rule applied: 세 실험을 모두 완료했으며 ACCEPT 유무와 관계없이 batch를 종료한다. 인접 parameter를 탐색하지 않는다.
- Candidate: R1-002를 development candidate로 유지한다. Final OOS는 계속 봉인한다.
