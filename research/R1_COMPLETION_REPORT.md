# R1 Completion Report

## Completion Status

`R1 COMPLETE — DEVELOPMENT RESEARCH ONLY`

R1은 Cross-sectional Momentum Rotation의 고정 baseline과 공통 evaluation protocol을 확립하고, 제한된 development 가설을 평가하는 목적을 달성했다. 2023–2025 Final OOS는 다운로드하거나 조회하지 않았다.

## Fixed Research Protocol

- Development: 2015-01-01–2022-12-31
- Final untouched OOS: 2023-01-01–2025-12-31
- Primary universe: AMD, TSLA, AMZN, AAPL
- Primary benchmark: SPY adjusted buy-and-hold
- Secondary benchmark: universe equal-weight buy-and-hold
- Initial cash: USD 100,000
- Primary cost: commission 0bps, one-way slippage 10bps
- Cost robustness: 0/5/10/20bps
- Signal/execution: close signal, next trading-day open execution
- Primary baseline: R1-001 Cross-sectional Momentum Rotation
- Development candidate: R1-002 126-day absolute-momentum risk-off

Universe는 ex-post selected이므로 selection/survivorship bias 가능성이 있다. Yahoo/yfinance adjusted data는 institutional-grade point-in-time dataset이 아니다.

## Experiment Outcomes

| ID | Hypothesis | Decision | Main finding |
|---|---|---|---|
| R1-001 | Existing Top 1 rotation baseline | `INCONCLUSIVE` | 높은 benchmark excess와 함께 -71.01% MDD, 기간·TSLA 집중 확인 |
| R1-002 | Winner 126-day momentum이 0 이하이면 cash | `ACCEPT — DEVELOPMENT HYPOTHESIS` | MDD, Sharpe, Calmar와 2021–2022 downside 대체로 개선 |
| R1-003 | Top 2 equal-weight | `REJECT` | 변동성과 MDD 감소, CAGR·Calmar와 realized-P&L concentration 악화 |
| R1-004 | 21-day score component 제거 | `INCONCLUSIVE` | 전체기간 개선과 최근 downside·concentration 악화가 충돌 |
| R1-005 | Volatility-adjusted score | `REJECT` | Concentration 개선, 전체 risk-adjusted 성과와 CAGR 보존 기준 실패 |
| R1-006 | Cross-sectional breadth gate | `REJECT` | Turnover·최근 downside 개선, risk-adjusted 성과와 concentration 악화 |
| R1-007 | SPY 126-day regime gate | `REJECT` | MDD·concentration 개선, Sharpe·Sortino·Calmar 악화 |

## Interpretation of R1-002

R1-002의 ACCEPT는 새로운 alpha 발견이 아니라 직관적인 risk-control rule이 development 데이터에서 실제로 일부 downside를 완화했는지 검증한 결과다. 과거 126-day return이 음수라는 사실이 이후 현금 수익이 우월함을 논리적으로 보장하지 않으므로 검증 자체는 필요했다.

이 판정은 다음만 의미한다.

- R1-002는 후속 robustness audit의 candidate로 유지할 근거가 있다.
- R1-001보다 development risk-control 특성이 대체로 낫다.
- Final OOS 성공, 최종 전략 채택 또는 paper/live readiness를 의미하지 않는다.

## Frozen Configurations

### R1-001 Primary Baseline

- Relative momentum lookbacks: 21/63/126 trading days
- Relative weights: 1/1/1
- Selection: Top 1
- Rebalance: every 5 trading days
- Absolute-momentum gate: none
- Execution: next open

### R1-002 Development Candidate

- R1-001 설정 유지
- Single addition: selected winner의 126-day absolute momentum이 `<= 0`이면 cash

R1 종료 후 이 설정을 R1 결과에 소급 반영하지 않는다. 이후 변경은 새 experiment ID와 별도 사전등록을 요구한다.

## R1 Stop Rule

- R1-003의 Top N/weight 조합을 추가 탐색하지 않는다.
- R1-004의 momentum weight/lookback을 추가 탐색하지 않는다.
- R1-005~R1-007의 volatility window, breadth threshold, regime lookback을 추가 탐색하지 않는다.
- Development 결과를 이용해 R1-001 또는 R1-002 정의를 소급 변경하지 않는다.
- R1은 추가 alpha experiment 없이 종료한다.

## Final OOS Double-confirmation Gate

Final OOS 개봉은 비가역적인 high-impact research decision으로 취급한다.

1. 일반적인 “연구를 계속해”, “OOS도 검증해” 또는 유사한 암시는 개봉 허가가 아니다.
2. 사용자가 `2023–2025 Final OOS를 개봉하라`고 명시적으로 요청해야 한다.
3. 그 요청 후에도 Quant Research Engineer가 개봉 범위와 반복 조회 금지 영향을 설명하고 두 번째 명시적 확인을 요청한다.
4. 사용자의 두 번째 확인 전에는 다운로드, 조회, 파일 생성 또는 결과 계산을 하지 않는다.

## Remaining Risks

- Ex-post universe selection 및 survivorship bias
- TSLA 중심 realized-P&L concentration
- 높은 절대 MDD와 최근 development downside
- Institutional-grade price, spread, market impact, tax, FX 부재
- 완전한 point-in-time universe 및 fundamentals 부재
- Final OOS 미검증

## R1 Conclusion

R1-001은 고정 research baseline, R1-002는 development candidate로 보존한다. R1-002는 최종 전략이 아니며 paper/live trading 근거로 사용하지 않는다. 다음 단계는 추가 parameter tuning이 아니라 candidate의 의존성, 재현성 및 robustness를 진단하는 R2다.
