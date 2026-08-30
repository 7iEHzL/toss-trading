# R2-003 — Overnight Gap Concentration

## Classification

`DISTRIBUTED`

R2-002에서 확인한 TSLA 2019–2020 overnight payoff가 소수 extreme gap에 의존하는지 진단했다. Frozen R1-002 10bps 결과만 사용했고 Final OOS는 조회하지 않았다.

## Pre-registered Rule

- `EXTREME_GAP_DRIVEN`: top 1 positive day ≥20% 또는 top 5 ≥50%
- `DISTRIBUTED`: top 5 <30%이고 positive overnight days ≥30
- `MIXED`: 그 사이

Threshold와 기간은 결과 확인 후 변경하지 않았다.

## Distribution Summary

| Metric | Result |
|---|---:|
| Overnight observation days | 302 |
| Positive days | 188 |
| Negative days | 114 |
| Positive contribution total | $14,131,072 |
| Negative contribution total | -$9,123,503 |
| Net overnight contribution | $5,007,569 |
| Mean per observation | $16,581 |
| Median per observation | $11,265 |
| Top 1 positive share | 4.65% |
| Top 5 positive share | 14.07% |
| Top 10 positive share | 23.39% |
| Positive contribution HHI | 0.0122 |

상위 5일 비중이 14.07%에 불과하고 양의 날이 188일이므로 `DISTRIBUTED` 조건을 충분히 충족한다.

## Largest Positive Overnight Days

| Rank | Date | Contribution |
|---:|---|---:|
| 1 | 2020-11-17 | $657,684 |
| 2 | 2020-12-01 | $378,724 |
| 3 | 2020-09-09 | $333,262 |
| 4 | 2020-09-18 | $309,521 |
| 5 | 2020-07-13 | $309,278 |
| 6 | 2020-02-04 | $278,472 |
| 7 | 2020-07-02 | $275,470 |
| 8 | 2020-12-03 | $267,721 |
| 9 | 2020-09-10 | $251,683 |
| 10 | 2020-10-22 | $243,474 |

가장 큰 음의 overnight contribution은 2020-09-08의 -$786,998로 가장 큰 양의 날보다 절대금액이 컸다. 전체 양의 payoff는 한 번의 극단적 상승보다 다수의 양의 날 누적으로 형성됐다.

## Combined R2 Interpretation

R2-001~003을 합치면 다음과 같다.

1. R1-002 development 성과는 TSLA 포함 여부에 의존한다.
2. TSLA 기여는 보유기간보다 payoff 크기에 의해 발생했다.
3. Payoff는 2019–2020 기간에 집중됐다.
4. 하지만 2019–2020 내부에서는 소수 extreme gap이 아니라 188개의 양의 overnight observation에 분산됐다.

따라서 정확한 표현은 “한두 번의 우연한 TSLA 급등”이 아니라 “2019–2020 TSLA의 지속적인 overnight 상승 국면에 대한 집중 노출”이다.

## Limitations and Stop Rule

- Dollar contribution은 당시 portfolio 규모와 보유수량의 영향을 받는다.
- 이 분석은 overnight return의 경제적 원인을 규명하지 않는다.
- 기간과 threshold를 추가 탐색하지 않는다.
- Overnight hedge, close execution 또는 universe 변경을 도입하지 않는다.
- Final OOS는 이중확인 gate로 봉인한다.
