# R5-000 — New Strategy Research Design

## Verdict

`DESIGN COMPLETE — RECOMMEND OPTION A; SECOND OPINION REQUIRED`

성과 계산이나 backtest 없이 새로운 strategy family 세 가지를 비교했다.

## Candidate Comparison

| Criterion | A. Independent trend + risk allocation | B. Cross-sectional momentum | C. Pure multi-asset risk allocation |
|---|---|---|---|
| Economic rationale | 행동적 underreaction/herding 및 느린 정보확산; 위험 균형 | 상대적 underreaction과 winner persistence | diversification 및 safer-asset risk-adjusted premium |
| R1–R4 failure 독립성 | 높음: ranking/Top-1 제거 | 낮음: winner concentration 구조 유지 | 높음: 수익예측과 winner 선택 없음 |
| Free-data feasibility | 높음: 고정 9 ETF의 OHLC만 필요 | 중간: 9 ETF는 가능하나 breadth가 작음 | 높음: 동일 고정 OHLC 사용 |
| Parameter freedom risk | 중간 | 중간~높음 | 낮음~중간 |
| Expected turnover/cost | 낮음~중간 | 중간~높음 | 낮음~중간 |
| Diversification | 높음, 단 동시 risk-off 가능 | 중간 이하 | 높음 |
| Falsifiability | 높음: no-trend/weighting ablation 가능 | 중간: ranking·Top N 선택 자유도 | 높음: EW 및 trend overlay와 분리 가능 |
| Interpretability | 높음 | 중간 | 높음 |
| Reproducibility | 높음 | 높음 | 높음 |
| Main failure risk | whipsaw, bond-dominated risk weights, crisis correlation | R1 반복, 작은 cross-section, regime crowding | low-vol concentration, no return edge, correlation spikes |

## Candidate A

- Economic rationale: 개별 시장의 1–12개월 return persistence는 행동적 underreaction과
  delayed overreaction으로 설명될 수 있고 여러 asset class futures에서 보고됐다.
- Expected advantages: 상대 순위와 winner-take-all을 제거하고, 다수 자산을 동시에 보유할
  수 있으며 signal과 allocation의 기여를 별도 baseline으로 분해할 수 있다.
- Failure risks: 횡보장에서 whipsaw, 장기채에 대한 inverse-volatility 집중, ETF proxy와
  futures 문헌 간 차이, 2007–2014의 짧은 표본.
- Free-data feasibility: 높음. 고정된 생존 ETF 9개의 adjusted OHLC만 요구한다.
- Parameter freedom: 중간. trend/volatility/rebalance 정의를 문헌에서 단일 규칙으로 고정해야 한다.
- Expected turnover: 낮음~중간.
- Interpretability: 높음.

## Candidate B

- Economic rationale: 강한 자산의 상대성과가 지속된다는 cross-sectional momentum.
- Expected advantages: 구현과 attribution이 명확하고 R1과 직접 비교 가능하다.
- Failure risks: R1/R2의 Top-1 concentration과 regime dependence를 구조적으로 재도입한다.
  9개 heterogeneous ETF는 relative ranking cross-section으로 작으며 category별 risk가 다르다.
- Free-data feasibility: 중간~높음.
- Parameter freedom: 중간~높음. lookback, Top N, weighting 자유도가 쉽게 증가한다.
- Expected turnover: 중간~높음.
- Interpretability: 중간.

## Candidate C

- Economic rationale: 동일 dollar weight보다 risk contribution을 분산하고 leverage-averse
  시장에서 safer assets의 상대적으로 높은 risk-adjusted return을 활용할 가능성.
- Expected advantages: 가장 단순하고 R1 실패와 독립적이며 낮은 turnover가 예상된다.
- Failure risks: 수익 방향 신호가 없어 장기 하락 자산을 계속 보유하며, inverse volatility가
  장기채·저변동 자산 집중을 새로 만들 수 있다.
- Free-data feasibility: 높음.
- Parameter freedom: 낮음~중간.
- Expected turnover: 낮음.
- Interpretability: 높음.

## Recommendation

Option A를 권고한다. Candidate C를 전략 구성요소이자 필수 structural baseline으로 두면
`trend가 가치를 만들었는가`와 `단순 위험배분이 가치를 만들었는가`를 분리할 수 있다.
Candidate B는 R1의 구조적 실패와 너무 가깝기 때문에 다음 primary question으로 부적합하다.

## Data Feasibility and Contamination

R4A universe의 가장 늦은 inception은 DBC의 2006-02-03이므로 2006년을 warm-up으로 두고
2007–2014를 별도 development 구간으로 제안한다. 이는 아직 가격 coverage를 검증하지
않은 feasibility 판단이며 다운로드 승인이 아니다. 2015–2022는 반복 관찰되어 clean
OOS가 아니며 secondary contaminated diagnostic으로만 사용할 수 있다. Final OOS
2023–2025는 SEALED다.

## Literature Basis

- Moskowitz, Ooi and Pedersen (2012), [*Time Series Momentum*](https://doi.org/10.1016/j.jfineco.2011.11.003),
  Journal of Financial Economics 104(2), 228–250.
- Hurst, Ooi and Pedersen (2017), [*A Century of Evidence on Trend-Following Investing*](https://doi.org/10.3905/jpm.2017.44.1.015),
  Journal of Portfolio Management 44(1), 15–29.
- Asness, Frazzini and Pedersen (2012), [*Leverage Aversion and Risk Parity*](https://doi.org/10.2469/faj.v68.n1.1),
  Financial Analysts Journal 68(1), 47–59.
- Moreira and Muir (2017), [*Volatility-Managed Portfolios*](https://doi.org/10.1111/jofi.12513),
  Journal of Finance 72(4), 1611–1644. 이는 별도 volatility-timing 가설의 근거이며
  R5-001에 혼합하지 않는다.

## Execution Record

- Performance calculations performed: 0
- Strategy backtests performed: 0
- Final OOS access: 0
- External price downloads: 0
- Broker/live-order calls: 0
