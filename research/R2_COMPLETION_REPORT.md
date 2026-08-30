# R2 Completion Report

## Status

`R2 COMPLETE — ROBUSTNESS AND DEPENDENCY AUDIT`

R2는 frozen R1-002의 수익을 개선하지 않고 development 성과의 종목·기간·가격경로·노출규모 의존성을 진단했다. Final OOS는 다운로드하거나 조회하지 않았다.

## Findings

| ID | Question | Result |
|---|---|---|
| R2-001 | 특정 종목 의존인가? | `CONCENTRATED`: TSLA 제외 시 CAGR -43.03%, Sharpe -0.259 |
| R2-002 | 보유기간·가격·거래·기간 중 원인은? | `PAYOFF_DRIVEN + PERIOD_CONCENTRATED` |
| R2-003 | 소수 extreme overnight gap인가? | `DISTRIBUTED`: top 5 positive share 14.07%, positive days 188 |
| R2-004 | Return edge와 capital scaling 중 무엇인가? | `CAPITAL_SCALING`; return edge는 hit-rate 기준을 0.013%p 하회 |

## Consolidated Explanation

R1-002의 높은 development 성과는 일반적인 종목 독립적 momentum 결과로 보기 어렵다. TSLA 포함 여부에 크게 의존하며, 특히 2019–2020의 지속적인 overnight 상승 국면에서 payoff가 발생했다. 이 payoff는 한두 번의 extreme gap이 아니라 많은 양의 overnight day에 분산됐다. 이후 복리로 커진 portfolio notional이 dollar contribution을 확대했다.

TSLA의 단위 노출당 overnight return도 다른 보유종목보다 높았지만 사전 `RETURN_EDGE` 기준 중 hit-rate 조건을 극소폭 통과하지 못했다. 이를 이유로 threshold를 변경하지 않았다.

## What R2 Does Not Establish

- R1-002가 다른 universe에서도 재현된다는 증거
- 2019–2020 TSLA regime가 반복된다는 증거
- Final OOS 성공 가능성
- 최종 candidate 선정 또는 paper/live readiness
- Overnight return의 경제적 원인

## Frozen Outcome

- R1-001: primary research baseline
- R1-002: development candidate, 최종 전략 아님
- R2 classification: TSLA-dependent, payoff/period-concentrated, internally distributed overnight gains, capital-scaled dollar P&L
- 추가 development attribution과 parameter tuning 종료
- Final OOS double-confirmation seal 유지

## Next Decision Boundary

다음 단계는 routine development 분석이 아니다. 새로운 survivorship-aware universe/data를 도입하거나 Final OOS 개봉 여부를 결정해야 하므로 high-impact second opinion이 필요하다. 사용자의 별도 결정 전까지 현재 candidate와 protocol을 변경하지 않는다.
