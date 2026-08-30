# R2-001 — Leave-one-out Universe Dependency Audit

## Classification

`CONCENTRATED`

이 결과는 전략 후보를 선택하는 실험이 아니라 frozen R1-002의 universe dependency audit다. Final OOS는 다운로드하거나 조회하지 않았다.

## Fixed Design

- Reference: frozen R1-002
- Development: 2015–2022
- Full universe: AMD, TSLA, AMZN, AAPL
- Diagnostic: 각 종목을 한 번씩 제외한 네 결과를 모두 측정
- Primary cost: 10bps; robustness 0/5/10/20bps
- Classification trigger: 단일 제외로 CAGR 30% 이상 감소, Sharpe 0.20 이상 감소 또는 benchmark excess 음수 전환
- Prohibition: 결과를 이용한 새 universe 선택 및 추가 subset search 금지

## 10bps Results

| Universe | CAGR | MDD | Sharpe | Sortino | Calmar | Turnover | Trades | SPY excess | Equal-weight excess |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Full R1-002 | 63.75% | -64.18% | 1.111 | 1.560 | 0.993 | 134.56x | 116 | 3,798.47%p | 3,101.67%p |
| AMD excluded | 48.49% | -60.63% | 1.080 | 1.348 | 0.800 | 107.29x | 90 | 1,716.00%p | 1,430.81%p |
| TSLA excluded | 36.32% | -50.31% | 0.852 | 1.219 | 0.722 | 130.24x | 124 | 804.46%p | 17.15%p |
| AMZN excluded | 54.02% | -61.63% | 1.006 | 1.421 | 0.877 | 113.18x | 96 | 2,323.76%p | 1,406.84%p |
| AAPL excluded | 67.47% | -60.63% | 1.142 | 1.586 | 1.113 | 103.81x | 98 | 4,533.70%p | 3,690.81%p |

## Dependency Triggers

TSLA 제외 시:

- CAGR: 63.75% → 36.32%, relative decrease 43.03%
- Sharpe: 1.111 → 0.852, decrease 0.259
- 두 benchmark excess는 양수지만 equal-weight excess가 3,101.67%p에서 17.15%p로 축소

CAGR 30% 감소 및 Sharpe 0.20 감소 trigger를 모두 충족하므로 `CONCENTRATED`로 분류한다.

## Cost Diagnostic — Sharpe

| Universe | 0bps | 5bps | 10bps | 20bps |
|---|---:|---:|---:|---:|
| AMD excluded | 1.106 | 1.093 | 1.080 | 1.054 |
| TSLA excluded | 0.884 | 0.868 | 0.852 | 0.819 |
| AMZN excluded | 1.027 | 1.016 | 1.006 | 0.985 |
| AAPL excluded | 1.164 | 1.153 | 1.142 | 1.121 |

비용 증가에 따라 Sharpe는 점진적으로 하락하며 dependency 방향은 뒤집히지 않는다.

## Concentration Diagnostic — 10bps

| Universe | Dominant symbol | Max absolute realized-P&L share |
|---|---|---:|
| Full R1-002 | TSLA | 71.49% |
| AMD excluded | TSLA | 81.61% |
| TSLA excluded | AMD | 43.95% |
| AMZN excluded | TSLA | 72.33% |
| AAPL excluded | TSLA | 83.16% |

TSLA가 포함된 세 leave-one-out universe에서는 TSLA가 계속 dominant realized-P&L source다.

## Interpretation

R1-002는 가격 기반 규칙으로 재현 가능하지만 development 성과는 종목 독립적이지 않다. TSLA를 제거해도 두 benchmark excess가 양수인 점은 momentum 방향의 완전한 소멸을 의미하지 않지만, CAGR과 Sharpe 감소 규모는 특정 종목 의존성을 명확히 보여준다.

AAPL 제외 결과가 개선됐다는 사실은 AAPL 제거의 근거로 사용하지 않는다. 그렇게 하면 audit 결과를 이용한 ex-post universe optimization이 된다.

## Stop Rule

- R2-001 종료
- 추가 두 종목 제외 조합 또는 최적 subset 탐색 없음
- Primary universe 및 frozen R1-002 변경 없음
- Final OOS 계속 봉인
