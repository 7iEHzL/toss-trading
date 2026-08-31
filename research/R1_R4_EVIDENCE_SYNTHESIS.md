# R1–R4 Evidence Synthesis

## Status

`SYNTHESIS COMPLETE — ORIGINAL CANDIDATE NOT PROMOTED; FINAL OOS SEALED`

이 문서는 R1부터 R4까지의 결과를 하나의 증거 사슬로 종합한다. 새로운 성과
실험이나 parameter 선택이 아니며, 기존 판정을 소급 변경하지 않는다.

## Original Claim Under Examination

Frozen R1-002는 21/63/126-day 상대 모멘텀으로 Top 1을 선택하고, winner의 126-day
절대 모멘텀이 0 이하이면 cash를 보유하는 전략이다. 처음의 강한 development 성과가
다음 중 무엇인지가 핵심 질문이었다.

1. 여러 종목과 자산에 일반화되는 momentum/risk-off edge
2. 사후 선택된 4개 종목, TSLA와 특정 historical regime에 의존한 결과

현재 증거는 두 번째 설명을 더 강하게 지지한다.

## Evidence Ladder

| Stage | Test | Result | Evidential meaning |
|---|---|---|---|
| R1 | Original four-stock development | 매우 높은 수익, R1-002 risk-off 일부 개선 | 가설 생성과 local development evidence |
| R1 robustness | Top 2, score/risk filters | 다수 REJECT, 일부 INCONCLUSIVE | 간단한 주변 변경으로 안정성이 쉽게 개선되지 않음 |
| R2 | Dependency and attribution | TSLA-dependent, 2019–2020 period/payoff concentrated, capital-scaled | 보편적 종목 독립 edge 설명 약화 |
| R3 | S&P 500 PIT replication feasibility | 무료 데이터 품질 부족으로 BLOCKED | 성과를 계산하지 않았으므로 긍정·부정 성과 증거가 아님 |
| R4A | Frozen nine-asset ETF replication | 10bps CAGR 1.39%, Sharpe 0.167, benchmark 열위; REJECT | 독립 asset-class 일반화 실패 |
| R4B | Broad ETF feasibility | 무료 historical master 부족으로 BLOCKED | broad cross-sectional claim은 미검증; survivor-only shortcut 거부 |

## What Remains Supported

- Original four-stock development sample에서 R1-002의 absolute-momentum cash gate는
  R1-001보다 MDD, Sharpe와 Calmar를 일부 개선했다.
- 해당 결과는 정확한 next-open execution, 비용 모델, portfolio accounting과 frozen
  protocol 아래 재현 가능한 local development observation이다.
- R2는 TSLA payoff가 한두 번의 extreme gap이 아니라 2019–2020의 여러 overnight
  상승일에 분산됐음을 보여줬다. 즉 단순 coding outlier로만 설명되지는 않는다.
- R4A에서는 단일 ETF absolute realized-P&L share가 26.62%로 낮아져 universe
  diversification이 concentration을 줄일 수 있다는 사실은 확인됐다.

이 증거는 연구 현상이 존재했다는 뜻이지, deployable alpha를 입증하지 않는다.

## What Was Rejected or Materially Weakened

- `R1-002 is a broadly generalizable momentum/risk-off edge`: R2 dependency와 R4A
  independent replication 결과에 의해 현재는 지지되지 않는다.
- `The original return is stock-independent`: TSLA 제외 시 성과가 크게 하락해 반증됐다.
- `The payoff is temporally stable`: 2019–2020 기여와 2021–2022 손실의 충돌로 약화됐다.
- `Diversification alone preserves the edge`: R1-003과 R4A에서 concentration은 줄었지만
  risk-adjusted benchmark 성과가 보존되지 않아 반증됐다.
- `The strategy is robust to realistic trading cost`: R4A는 0bps 40.13%에서 20bps
  -10.99%로 악화됐고 10bps에서도 benchmark에 크게 미달했다.
- Paper/live readiness 또는 final candidate 지위: 근거 없음.

## What Remains Unknown

- Final OOS 2023–2025 결과
- 완전한 survivorship-aware stock 또는 broad-ETF universe에서의 결과
- 다른 독립 시장·국가·더 긴 기간에서의 재현성
- TSLA overnight payoff의 지속 가능한 경제적 원인
- 다른 전략 family의 성과

R3와 R4B는 데이터 gate에서 중단됐으므로 `negative performance evidence`로 해석하지
않는다. 반대로 데이터가 없다는 이유로 generalization을 가정하지도 않는다.

## Candidate Disposition

- R1-001은 historical primary baseline으로 보존한다.
- R1-002는 frozen historical development candidate와 research case study로 보존하되,
  active candidate pipeline에서는 승격하지 않는다.
- R1-002에 대한 추가 Top N, lookback, score weight, risk gate 또는 cost-dependent
  tuning을 종료한다.
- 현재 증거로 Final OOS를 개봉하거나 paper/live 단계로 이동하지 않는다.
- 코드와 결과는 삭제하지 않는다. 향후 research-process regression 또는 새로운 전략의
  비교 control로 사용할 수 있지만 이를 재승인으로 해석하지 않는다.

## Was the Project Successful?

연구 결과가 전략 채택으로 이어지지는 않았지만 research process는 성공적으로 작동했다.

- 처음의 수천 퍼센트 수익을 최종 결론으로 채택하지 않았다.
- 동일 development data에서 무제한 parameter search를 하지 않았다.
- dependency, price path, period와 capital scaling을 분리했다.
- frozen rule을 독립 asset universe에 적용해 일반화 주장을 실제로 반증할 기회를 줬다.
- 데이터 품질을 충족하지 못한 R3/R4B에서는 성과를 만들지 않았다.
- Final OOS를 반복 확인하지 않고 보존했다.

이는 높은 backtest return보다 더 중요한 프로젝트 자산이다.

## Is New Strategy Research Worthwhile?

`YES`, 단 R1-002의 인접 parameter tuning이 아니라 새로운 연구 질문이어야 한다.
새 단계는 다음 조건을 충족해야 한다.

1. 경제적 rationale과 실패 가능한 가설을 코드 수정 전에 작성한다.
2. 데이터와 universe를 가격 성과보다 먼저 확정한다.
3. 무료 데이터로도 inactive-security 문제가 작거나 명시적으로 측정 가능한 대상을 고른다.
4. Top-1 concentration과 5-day high-turnover 구조를 당연한 전제로 두지 않는다.
5. turnover와 cost capacity를 primary success criterion에 포함한다.
6. 여러 자산·기간의 contribution과 benchmark 우위를 함께 요구한다.
7. 기존 2015–2022 결과를 반복 탐색한 test set처럼 사용하지 않는다.
8. Final OOS는 최종 사전등록 candidate가 충분한 independent evidence를 확보할 때까지
   열지 않는다.

## Recommended Next Stage

다음 단계는 `R5-000 — New Strategy Research Question Selection`이다. R5-000에서는
성과를 실행하지 않고 서로 독립적인 2–3개 strategy family의 economic rationale,
필요 데이터, expected turnover, primary failure mode와 falsification test를 비교한다.

R5는 R1-002를 개선하는 단계가 아니다. 한 family를 선택한 후에만 별도 R5-001
protocol을 사전등록한다. Final OOS 2023–2025는 계속 SEALED 상태로 유지한다.
