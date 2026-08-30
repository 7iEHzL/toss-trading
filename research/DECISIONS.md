# Research Decisions

이 문서는 기존 plan, log와 결과 보고서에서 확인되는 주요 결정을 시간 순서로 요약한다. 상세 수치와 실험 기록은 `RESEARCH_LOG.md` 및 `research/results/`를 따른다.

## D-001 — P1 Research-ready Baseline

- Decision: 현재 backtester를 institutional-grade가 아닌 research-ready baseline으로 간주한다.
- Rationale: 공통 execution cost, next-open execution, portfolio accounting, benchmark와 표준 metrics가 마련되었지만 survivorship-free universe와 point-in-time fundamentals는 구축되지 않았다.
- Consequence: 편향을 숨기지 않고 명시하며 R1 factor research를 시작한다.

## D-002 — R1 Primary Baseline and Protocol

- Decision: Cross-sectional Momentum Rotation을 primary baseline으로 고정한다.
- Rationale: 가격 데이터만 사용하고 factor contribution을 분리해 해석하기 쉽다.
- Scope: AMD, TSLA, AMZN, AAPL. SPXL은 robustness 전용이며 Multifactor v2는 후속 candidate로 보존한다.
- Evaluation: 2015–2022 development, SPY primary benchmark, universe equal-weight secondary benchmark, slippage 0/5/10/20bps.
- Seal: 2023–2025 Final OOS는 연구 iteration 동안 조회하지 않는다.
- Known limitation: universe의 ex-post selection bias.

## D-003 — R1-001 Baseline Evaluation

- Decision: `INCONCLUSIVE`; 성과가 높지만 안정적인 전략으로 승인하지 않는다.
- Rationale: 비용 조건에서 benchmark를 초과했지만 MDD -71.01%, 2021–2022 큰 손실, 높은 turnover와 TSLA 실현손익 집중이 확인되었다.
- Consequence: baseline은 소급 변경하지 않고 진단 기준으로 유지한다.

## D-004 — R1-002 Absolute-momentum Risk-off

- Decision: `ACCEPT — DEVELOPMENT HYPOTHESIS ONLY`.
- Rationale: 기존 winner의 126-day absolute momentum이 0 이하일 때 cash를 보유하는 단일 변경이 MDD, Sharpe, Calmar와 2021–2022 downside를 대체로 개선했고 비용별 방향도 유지했다.
- Limitation: Sortino는 소폭 악화했고 절대 MDD와 TSLA 집중은 여전히 크다.
- Consequence: R1-002를 development candidate로 유지하되 최종 전략으로 채택하지 않는다.

## D-005 — R1-003 Top 2 Equal-weight

- Decision: `REJECT`.
- Rationale: MDD와 volatility는 개선되었지만 CAGR, Sortino, Calmar가 하락했고 거래원장 기준 최대 단일 종목 절대 실현손익 비중이 71.49%에서 80.03%로 악화되었다.
- Consequence: R1-002를 candidate로 유지하며 Top 3 또는 다른 weight를 즉시 탐색하지 않는다.

## D-006 — Autonomous Research Governance

- Decision: Routine factor selection, experiment priority, development 판정과 후속 단일 가설 설계는 Quant Research Engineer가 자율 수행한다.
- Rationale: 반복적인 routine decision보다 사전 등록과 persistent context를 통해 연구 일관성을 유지한다.
- Second opinion boundary: Final OOS 개봉, baseline/protocol 사후 변경, parameter search 확대, 충돌하는 강한 증거, 새로운 데이터/ML, 최종 candidate 선정, paper/live 전환.

## D-007 — R1-004 Short-horizon Component Removal

- Decision: `INCONCLUSIVE`.
- Rationale: 21-day score 항 제거는 전체 development에서 Sharpe, Sortino, Calmar, CAGR과 turnover를 개선했지만 2021–2022 downside와 TSLA realized-P&L concentration을 악화시켰다.
- Consequence: R1-004를 채택하거나 폐기하지 않고 보존한다. R1-002가 development candidate로 유지되며 인접 weight/lookback을 추가 탐색하지 않는다.
- Protocol impact: 없음. Final OOS는 계속 봉인한다.

## D-008 — Bounded Development Batch Option A

- Decision: R1-005~R1-007 세 독립 가설을 결과 조회 전에 일괄 고정하고 모두 평가한다.
- Rationale: ACCEPT가 나올 때까지 결과 종속적으로 반복하는 대신 명시적인 실험 수와 공통 판정 기준으로 data snooping을 제한한다.
- Scope: volatility-adjusted score, cross-sectional breadth gate, SPY market-regime gate. 모두 R1-002와 독립 비교한다.
- Stop rule: 세 실험 후 ACCEPT 유무와 관계없이 batch 종료. 인접 parameter 탐색 없음.
- Seal: Final OOS 2023–2025는 계속 봉인한다.

## D-009 — Bounded Batch Outcome

- R1-005 volatility-adjusted score: `REJECT`. Concentration과 최근 downside 개선보다 전체 risk-adjusted 성과 저하 및 CAGR 보존 기준 미달이 우세했다.
- R1-006 breadth gate: `REJECT`. Turnover와 최근 downside는 개선됐지만 전체 Sharpe/Sortino/Calmar와 concentration이 악화됐다.
- R1-007 SPY regime gate: `REJECT`. MDD와 concentration은 개선됐지만 전체 Sharpe/Sortino/Calmar가 공통 허용 범위를 초과해 악화됐다.
- Decision: 세 실험 중 ACCEPT 없음. R1-002를 development candidate로 유지한다.
- Stop rule: bounded batch 종료. 인접 parameter search 및 Final OOS 개봉 없음.

## D-010 — R1 Closure

- Decision: R1을 추가 alpha experiment 없이 공식 종료한다.
- Frozen state: R1-001 primary baseline, R1-002 development candidate.
- Rationale: baseline protocol과 제한된 가설 평가가 완료됐고 같은 development 데이터의 추가 탐색은 data snooping 위험을 높인다.
- Interpretation: R1-002 ACCEPT는 risk-control validation이며 최종 candidate 선정이나 OOS 성공을 의미하지 않는다.
- Next stage: R2 robustness and dependency audit.

## D-011 — Final OOS Double-confirmation

- Decision: Final OOS 개봉에는 두 번의 명시적 사용자 확인이 필요하다.
- First gate: 사용자가 `2023–2025 Final OOS를 개봉하라`고 직접 요청.
- Second gate: 개봉 범위와 비가역성 안내 후 사용자가 다시 명시적으로 확인.
- Consequence: 암시적 요청이나 일반적인 OOS 언급만으로는 다운로드·조회하지 않는다.

## D-012 — R2-001 Universe Dependency

- Classification: `CONCENTRATED`.
- Evidence: TSLA 제외 시 CAGR이 약 43.03% 감소하고 Sharpe가 0.259 하락해 사전 dependency trigger를 충족했다.
- Interpretation: R1-002의 development 성과는 TSLA 포함 여부에 실질적으로 의존한다.
- Non-decision: AAPL 제외 성과가 개선됐지만 이를 근거로 universe를 변경하지 않는다.
- Stop rule: leave-one-out audit 종료. 추가 subset search 및 Final OOS 개봉 없음.

## D-013 — R2-002 P&L Source Attribution

- Classification: `PAYOFF_DRIVEN + PERIOD_CONCENTRATED`.
- Exposure evidence: TSLA holding-day share 34.49%는 AMD 38.84%보다 낮지만 absolute net contribution share는 71.49%다.
- Price-path evidence: TSLA overnight contribution +$7.34M, intraday contribution -$2.59M.
- Period evidence: TSLA 2019–2020 +$8.34M, 2021–2022 -$3.68M.
- Trade evidence: 최대 단일 realized trade share 21.09%로 30% threshold 미달.
- Consequence: dependency는 장기 보유나 단일 거래보다 TSLA의 특정 기간 overnight payoff에 의해 발생했다. 전략 변경 근거로 직접 사용하지 않는다.

## D-014 — R2-003 Overnight Gap Distribution

- Classification: `DISTRIBUTED` within 2019–2020.
- Evidence: 188 positive overnight days; top 1/5/10 positive shares 4.65%/14.07%/23.39%; positive HHI 0.0122.
- Interpretation: TSLA contribution은 2019–2020 기간에 집중됐지만 소수 extreme gap 한두 개에 의존하지 않았다.
- Consequence: close execution, overnight hedge 또는 threshold 변경 근거로 사용하지 않는다.

## D-015 — R2-004 Exposure-normalized Attribution

- Classification: `CAPITAL_SCALING`.
- Evidence: TSLA 2019–2020 average notional은 pooled others의 3.94배로 1.5배 threshold를 충족.
- Return diagnostic: mean overnight return은 +0.279%p/day 높았지만 hit-rate 차이는 +4.987%p로 5%p threshold를 0.013%p 하회.
- Decision discipline: 경계 결과를 이유로 threshold를 완화하지 않고 `RETURN_EDGE`를 부여하지 않는다.
- Consequence: R2 attribution 종료. Position sizing, execution과 universe는 변경하지 않는다.

## D-016 — R2 Closure

- Decision: R2를 R2-004에서 종료한다.
- Findings: R1-002는 TSLA dependent이며, 2019–2020의 분산된 overnight payoff와 커진 notional의 영향을 받았다.
- Limitation: development evidence와 ex-post universe이므로 최종 candidate 또는 OOS 성공을 의미하지 않는다.
- Next gate: 새로운 데이터/방법론 또는 Final OOS는 high-impact second opinion 대상. Final OOS는 이중확인 상태로 봉인.

## D-017 — R3-000 PIT Data Feasibility

- Decision: `CONDITIONAL — R3-001 NOT AUTHORIZED`.
- Evidence: Norgate Platinum/Diamond와 S&P SPICE + CRSP는 공식 문서상 historical S&P 500 membership, delisted securities, OHLC, corporate-action 및 permanent-ID 요구를 충족할 가능성이 있다.
- Current limitation: 프로젝트에는 해당 라이선스와 실제 sample access가 없으며 ticker mapping, delisting treatment, point-in-time effective dates와 immutable snapshot을 row level에서 검증하지 못했다.
- Rejected shortcut: 현재 S&P 500 구성종목 목록과 Yahoo/yfinance 가격으로 과거 universe를 재구성하지 않는다.
- Consequence: 데이터 sample audit가 mandatory gate 전부를 통과하기 전에는 R3-001을 실행하지 않는다. Option B 전환 또는 상용 데이터 확보는 별도 high-impact decision이다.
- Protocol: R1-002 parameters는 동결하고 Final OOS 2023–2025는 계속 봉인한다.

## D-018 — R3 Free-data Audit Outcome

- Decision: `BLOCKED — DATA QUALITY INSUFFICIENT`; R3-001 not authorized.
- Data: pitindex 0.2.1 bundled membership and Yahoo/yfinance 1.7.0 adjusted OHLCV, 2014-07-01 through 2023-01-01 exclusive.
- Evidence: 701 PIT tickers 중 427개 가격 확보(60.91%), unresolved 274개, constituent-date coverage 63.58%. Membership count 498–507과 manifest hash는 통과했으며 Final OOS 행은 0개.
- Interpretation: 성과 결과가 아니라 무료 데이터 품질 실패다. Yahoo 실패 메시지로 delisting/merger를 자동 판정하지 않는다.
- Discipline: 98%/99%/1% 사전 gate를 완화하지 않고 missing ticker를 silent drop하지 않는다. 추가 대규모 retry나 여러 fallback source 혼합으로 결과를 강제하지 않는다.
- Consequence: pitindex + Yahoo S&P 500 replication 경로를 종료한다. Fixed ETF universe 전환은 별도 사전등록과 second opinion이 필요한 high-impact decision이다.
- Seal: Frozen R1-002는 변경하지 않았고 Final OOS 2023–2025는 계속 봉인한다.

## D-019 — Final R3 Clean Retry and Closure

- Decision: clean retry calibration failed; `R3 CLOSED — BLOCKED BY FREE-DATA QUALITY`.
- Evidence: seed-fixed previous-missing sample 0/30 recovered; 37 calibration/control requests 중 success 3, invalid payload 9, price not returned 25. AAPL mandatory control도 총 3회 후 실패.
- Full audit: 선행 calibration gate 실패로 701-ticker clean full audit을 실행하지 않음.
- Attribution: 최초 4.1%에는 validator defect, 기존 60.91%에는 batch/checkpoint artifact가 있었지만 clean sample은 Yahoo historical/delisted limitation과 payload instability가 독립적으로 남음을 확인.
- Discipline: 추가 retry, manual mapping, fallback price-source mixing, threshold 완화, missing 제거 없음.
- R3-001: current free-data protocol에서 permanently `NOT AUTHORIZED`. Institutional/PIT dataset 도입 시에만 새로운 decision으로 재개 가능.
- Next stage: R4 fixed-ETF 연구 질문과 category-first selection protocol만 설계. Performance not run.
- Seal: R1-002 unchanged; Final OOS 2023–2025 SEALED.

## D-020 — R3 Closure Confirmed and R4-000 Authorized

- Decision: Option A approved. R3 is final as `R3 CLOSED — BLOCKED BY FREE-DATA QUALITY`; no additional free S&P 500 retry is allowed.
- R4 question: replicate frozen R1-002 on a category-first fixed ETF universe, without treating R4 as a substitute stock-level PIT replication.
- Pre-registration: nine economic categories, inception before 2010-01-01, 2013 median daily dollar volume at least USD 5 million, maximum-liquidity representative per category, deterministic tie-breaks, universe freeze 2014-06-30.
- R4-000 scope: non-price eligibility, data-quality/liquidity audit and final universe freeze only. Strategy performance is prohibited.
- Discipline: category, candidate roster and thresholds are not changed because a selected ETF looks unintuitive or because audit results are inconvenient.
- Frozen items: R1-002 parameters unchanged; Final OOS 2023–2025 remains SEALED.
- Next decision: R4-001 performance replication requires a new authorization after R4-000 adjudication.

## D-021 — R4-000 Universe Freeze

- Decision: R4-000 passed its pre-registered eligibility and data-quality gate.
- Frozen universe: SPY, EFA, EEM, IEF, TLT, LQD, IYR, GLD and DBC, one representative for each of the nine categories.
- Selection basis: maximum 2013 median raw-close dollar volume among candidates passing the USD 5M and coverage rules. No tie-break was needed.
- Data evidence: 30/31 candidates returned valid pre-freeze data; all returned frames had 100% common-SPY-calendar coverage in both audit subperiods. TLO returned no Yahoo payload and remains an explicit ineligible data failure.
- Integrity: snapshot manifest verified with zero mismatches; 0 rows on or after 2023-01-01; strategy performance was not run.
- Limitation: the pre-registered issuer-family roster is a closed practical roster, not a complete historical census of every U.S.-listed ETF.
- R4-001: eligible for a separate authorization decision, but not yet authorized or executed.
- Seal: frozen R1-002 unchanged; Final OOS 2023–2025 SEALED.
