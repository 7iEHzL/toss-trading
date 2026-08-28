# R1 Baseline Strategy Research Plan

## Status

`BASELINE_LOCKED — DEVELOPMENT DATA PENDING`

Second opinion 결정에 따라 Cross-sectional Momentum Rotation을 primary baseline으로 확정했다. 저장소에는 장기 로컬 가격 데이터와 benchmark snapshot이 없으므로 실제 성과 수치는 아직 산출하지 않는다.

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
