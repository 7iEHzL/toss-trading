# Research Log

성공·실패·불확실한 결과를 모두 기록한다. Final OOS를 확인한 뒤 가설이나 판정 기준을 소급 변경하지 않는다.

## R1-000 — Baseline Planning

- ID: `R1-000`
- Hypothesis: 단순하고 해석 가능한 기존 전략을 factor 연구 baseline으로 고정할 수 있다.
- Baseline: 미선정
- Change: 코드 및 전략 변경 없음
- Experiment setup: 저장소 구조와 기존 후보를 정적으로 비교. 외부 API 호출 없음.
- Results: 로컬 장기 데이터와 benchmark가 없어 정량 비교 불가. 후보는 가격 기반 Rotation과 Multifactor v2로 축소.
- Conclusion: `INCONCLUSIVE`; baseline과 데이터 명세에 second opinion 필요.
- Next research question: 가격-only Rotation과 정적 펀더멘털을 포함한 Multifactor v2 중 어느 것을 R1 baseline으로 사용할 것인가?

## R1-000A — Second Opinion Decision

- ID: `R1-000A`
- Hypothesis: 가격-only Rotation이 후속 factor contribution을 측정하기 위한 더 깨끗한 baseline이다.
- Baseline: Cross-sectional Momentum Rotation 확정
- Change: primary universe에서 SPXL 제외. SPXL은 robustness에만 포함. Multifactor v2는 후속 candidate로 보존.
- Experiment setup: development/walk-forward 2015–2022, final untouched OOS 2023–2025, SPY primary benchmark, universe equal-weight buy-and-hold secondary benchmark, slippage 0/5/10/20bps.
- Results: 연구 설계 결정만 완료. 성과 데이터는 아직 조회하지 않음.
- Conclusion: `ACCEPT` — baseline 및 평가 규칙 고정. Universe의 ex-post selection bias는 명시적으로 유지.
- Next research question: 개발 구간에서 기존 Rotation parameter가 benchmark 및 비용 변화에 대해 어떤 성과와 취약성을 보이는가?

## R1-001 — Development Baseline Evaluation

- ID: `R1-001`
- Hypothesis: 기존 Rotation baseline은 2015–2022 development 영역에서 비용 적용 후에도 benchmark 대비 해석 가능한 성과를 보인다.
- Baseline: AMD/TSLA/AMZN/AAPL Cross-sectional Momentum Rotation
- Change: alpha/parameter 변경 없음
- Experiment setup: Yahoo/yfinance 1.2.0 adjusted OHLC, 2015-01-02~2022-12-30, primary universe AMD/TSLA/AMZN/AAPL, SPY 및 동일가중 benchmark, 0/5/10/20bps.
- Results: 10bps에서 누적수익률 3,558.20%, CAGR 61.75%, Sharpe 1.079, MDD -71.01%, turnover 142.06x. SPY 112.17%, 동일가중 808.97%. 2021–2022 수익률 -63.8%, Sharpe -0.75. 실현손익이 TSLA에 크게 집중. SPXL robustness는 수익을 높였지만 leverage effect와 분리 불가.
- Conclusion: `INCONCLUSIVE`
- Next research question: 기존 baseline을 결함이 명확한 진단 기준으로 유지할지, 항상 risk-on 구조를 분리하기 위한 단순 risk-control control을 추가할지 결정.

## R1-001A — Second Opinion Decision

- ID: `R1-001A`
- Hypothesis: 결함이 확인된 R1-001도 소급 변경하지 않은 고정 research baseline으로 가치가 있다.
- Baseline: R1-001 Cross-sectional Momentum Rotation 유지
- Change: baseline 변경 없음. SPY와 동일가중 buy-and-hold benchmark 유지.
- Experiment setup: 다음 실험은 기존 126일 absolute momentum을 사용한 단일 cash risk-off filter. TSLA 제외는 diagnostic으로만 사용.
- Results: 연구 방향 결정 완료. Final OOS 미조회.
- Conclusion: `ACCEPT`
- Next research question: 126일 absolute momentum risk-off가 development downside와 risk-adjusted metric을 개선하는가?

## R1-002 — 126-day Absolute Momentum Risk-off

- ID: `R1-002`
- Hypothesis: 선택된 winner의 126일 momentum이 0 이하일 때 현금을 보유하면 baseline의 MDD와 약세 구간 손실이 개선된다.
- Baseline: R1-001 primary baseline
- Change: winner 126-day absolute momentum `<= 0`일 때 cash
- Experiment setup: R1-001과 동일. TSLA 제외 diagnostic 추가. Final OOS 봉인.
- Results: 10bps에서 return 3,910.64%, MDD -64.18%, Sharpe 1.111, Sortino 1.560, Calmar 0.993, turnover 134.56x. Baseline 대비 MDD +6.83%p, Sharpe +0.032, Calmar +0.123, 2021–2022 return -63.8%→-56.5%. Sortino는 -0.020. TSLA 제외 비교에서도 MDD -57.93%→-50.31%, Sharpe 0.809→0.852, Calmar 0.586→0.722.
- Conclusion: `ACCEPT` — development 가설 승인. Final candidate 채택은 아님.
- Next research question: 남은 핵심 문제인 종목 집중을 직접 다룰지, R1-002를 고정 candidate로 두고 다른 독립 factor 연구로 이동할지 결정.

## R1-003 — Top 2 Equal-weight Diversification

- ID: `R1-003`
- Hypothesis: R1-002의 Top 1을 Top 2 equal-weight로만 바꾸면 single-name concentration과 MDD를 낮추면서 momentum premium의 상당 부분을 보존할 수 있다.
- Baseline: R1-002 126-day absolute-momentum risk-off.
- Change: Top 1 → Top 2, 각 slot 50%. 각 후보의 126-day momentum이 0 이하이면 해당 slot은 cash.
- Experiment setup: 2015–2022 development snapshot, AMD/TSLA/AMZN/AAPL, SPY 및 universe equal-weight benchmark, next-open execution, slippage 0/5/10/20bps. 다른 parameter는 변경하거나 탐색하지 않는다. Final OOS는 봉인한다.
- Success criteria: MDD뿐 아니라 Sharpe/Calmar, realized-P&L concentration, CAGR 및 excess-return 보존을 함께 판단한다.
- Results: 10bps에서 R1-002 대비 MDD -64.18%→-47.57%, volatility 60.42%→39.95%, Sharpe 1.111→1.125로 개선되었다. 반면 CAGR 63.75%→44.74%, Sortino 1.560→1.490, Calmar 0.993→0.941로 하락했다. 최대 단일 종목 절대 realized-P&L share는 TSLA 기준 71.49%→80.03%로 상승했다. 2021–2022 손실은 -56.48%→-27.74%로 완화되었고, 10bps excess return은 SPY 대비 1,380.21%p, equal-weight 대비 683.41%p로 양수를 유지했다. 결과 방향은 0/5/10/20bps에서 일관되었다.
- Conclusion: `REJECT` — downside는 개선했지만 Calmar와 Sortino 및 명시적 P&L concentration 기준을 함께 충족하지 못했고 CAGR 희생도 컸다.
- Next research question: Top 3나 weight 조합을 재튜닝하지 않는다. R1-002를 development candidate로 유지하고 다음 독립 factor research question을 사전 등록한다.

## R1-004 — Remove Short-horizon Momentum Component

- ID: `R1-004`
- Hypothesis: R1-002 score에서 21-day 항만 제거하면 단기 가격 민감도와 집중을 낮추면서 63/126-day momentum premium을 보존할 수 있다.
- Baseline: R1-002 126-day absolute-momentum risk-off.
- Change: relative momentum weights 1/1/1 → 0/1/1.
- Experiment setup: 기존 R1 protocol과 동일. Top 1, 126-day risk-off, 5일 rebalance와 next-open execution 유지. 다른 parameter search 없음. Final OOS 봉인.
- Success criteria: Sharpe/Calmar 비열화, turnover 또는 realized-P&L concentration 개선, CAGR 및 benchmark excess return 보존, 비용·시간 구간상 심한 충돌 없음.
- Results: 10bps 전체 development에서 R1-002 대비 CAGR 63.75%→79.47%, Sharpe 1.111→1.267, Sortino 1.560→1.786, Calmar 0.993→1.198, turnover 134.56x→116.82x로 개선되었다. 반면 MDD는 -64.18%→-66.36%, 최대 single-name absolute realized-P&L share는 TSLA 기준 71.49%→73.77%로 악화됐다. 2015–2020의 세 2년 구간에서는 대체로 개선됐지만 2021–2022 return -56.48%→-59.13%, Sharpe -0.672→-0.762로 악화됐다. 비용별 전체기간 개선 방향은 0/5/10/20bps에서 유지됐다.
- Conclusion: `INCONCLUSIVE` — 전체기간 risk-adjusted 성과와 turnover 개선은 강하지만 최근 development downside 및 concentration 악화와 충돌한다.
- Next research question: 인접 weight/lookback을 재탐색하지 않는다. R1-002를 candidate로 유지하고, 이 충돌을 이용해 protocol을 사후 변경하거나 Final OOS를 열지 않는다.

## R1-005–R1-007 — Bounded Batch (Pre-registered)

- Decision: Option A 승인. 세 독립 가설을 결과 전에 고정하고 모두 평가한 뒤 batch 종료.
- Baseline: 각 실험별 R1-002.
- Common setup: 기존 R1 protocol, 10bps primary와 0/5/10/20bps robustness, 2년 구간 및 concentration diagnostic, Final OOS 봉인.
- Common criteria: Sharpe/Sortino/Calmar 중 2개 이상 개선, 0.05 초과 악화 없음, MDD 악화 3%p 이내, CAGR 80% 이상 보존, benchmark excess 양수, turnover 증가 20% 이내.
- R1-005 change: 기존 score를 trailing 63-day volatility로 조정.
- R1-006 change: 126-day positive breadth가 2/4 미만이면 cash.
- R1-007 change: SPY 126-day momentum이 0 이하이면 cash.
- Stop rule: ACCEPT 여부와 무관하게 세 실험 후 종료하며 인접 parameter를 탐색하지 않음.
- Results: R1-005는 10bps CAGR 48.74%, Sharpe 0.987, Sortino 1.355, Calmar 0.776, MDD -62.81%, concentration 63.96%. R1-006은 CAGR 59.87%, Sharpe 1.086, Sortino 1.455, Calmar 0.932, MDD -64.24%, concentration 86.13%. R1-007은 CAGR 52.05%, Sharpe 1.038, Sortino 1.318, Calmar 0.910, MDD -57.20%, concentration 66.78%. 세 실험 모두 비용별 방향은 일관됐고 2021–2022 downside 일부를 개선했지만 공통 risk-adjusted 필수 기준을 통과하지 못했다.
- Conclusions: R1-005 `REJECT`; R1-006 `REJECT`; R1-007 `REJECT`.
- Stop rule: batch 완료. 추가 volatility window, breadth threshold, regime lookback을 탐색하지 않는다. R1-002 candidate와 Final OOS seal을 유지한다.

## R2-001 — Leave-one-out Universe Dependency Audit

- ID: `R2-001`
- Hypothesis: R1-002가 특정 단일 종목에 과도하게 의존하지 않는다면 각 종목 제외 후에도 risk-adjusted 성과와 benchmark excess 방향이 유지된다.
- Baseline: Frozen R1-002.
- Change: 전략 변경 없음. AMD, TSLA, AMZN, AAPL을 각각 한 번 제외하는 audit-only diagnostic.
- Experiment setup: 2015–2022 development, 0/5/10/20bps, Final OOS 봉인. 결과를 universe selection에 사용하지 않음.
- Classification rule: 단일 제외로 CAGR 30% 이상 감소, Sharpe 0.20 이상 감소 또는 benchmark excess 음수 전환 시 `CONCENTRATED`.
- Results: TSLA 제외 시 CAGR 63.75%→36.32%(-43.03%), Sharpe 1.111→0.852(-0.259), equal-weight excess 3,101.67%p→17.15%p. AMD 제외 CAGR 48.49%, AMZN 제외 54.02%, AAPL 제외 67.47%. 모든 제외 결과의 SPY 및 equal-weight excess는 양수 유지.
- Conclusion: `CONCENTRATED` — TSLA exclusion이 사전 trigger 두 개를 충족.
- Stop rule: 추가 subset 제거 또는 universe 재선정 없음.

## R2-002 — P&L Source Attribution

- ID: `R2-002`
- Research question: R1-002 TSLA dependency가 가격 노출, 보유 기간, 소수 대형 거래 또는 특정 기간 중 어디서 발생하는가?
- Baseline: Frozen R1-002 10bps.
- Change: 전략 변경 없음. Exact daily P&L attribution만 추가.
- Experiment setup: overnight/intraday price contribution과 execution cost를 종목별 분해하고 equity delta와 reconcile. Holding days, sell realized P&L과 2년 구간 기여도 진단. Final OOS 봉인.
- Interpretation thresholds: single trade absolute realized-P&L 30%, single period positive contribution 60%, exposure/payoff 비교.
- Results: TSLA holding-day share 34.49%, absolute net contribution share 71.49%, gross path share 68.24%. TSLA overnight +$7.34M, intraday -$2.59M, cost -$0.11M, net +$4.64M. 2019–2020 +$8.34M, 2021–2022 -$3.68M. 최대 단일 realized trade +$3.64M은 absolute realized-P&L의 21.09%. Reconciliation 최대 $1.6e-9.
- Conclusion: `PAYOFF_DRIVEN + PERIOD_CONCENTRATED`; `TRADE_OUTLIER_DRIVEN` 아님. AMD가 더 오래 보유됐으므로 단순 exposure duration 설명도 기각.
- Stop rule: attribution 결과를 이용한 universe, execution timing 또는 parameter 변경 없음.

## R2-003 — Overnight Gap Concentration

- ID: `R2-003`
- Research question: TSLA 2019–2020 overnight payoff가 소수 extreme gap 또는 다수 분산된 gap 중 어디서 발생했는가?
- Baseline: Frozen R1-002 10bps attribution.
- Change: 전략 변경 없음. Positive overnight contribution의 top 1/5/10 share와 HHI 진단.
- Classification: top 1 ≥20% 또는 top 5 ≥50%면 `EXTREME_GAP_DRIVEN`; top 5 <30% 및 positive days ≥30이면 `DISTRIBUTED`; 나머지는 `MIXED`.
- Results: 302 overnight observation 중 positive 188, negative 114. Positive total +$14.13M, negative -$9.12M, net +$5.01M. Top 1/5/10 positive share 4.65%/14.07%/23.39%, HHI 0.0122. 최대 양의 날은 2020-11-17 +$657,684, 최대 음의 날은 2020-09-08 -$786,998.
- Conclusion: `DISTRIBUTED`. 2019–2020 기간에는 집중됐지만 기간 내부 payoff는 소수 extreme gap이 아닌 다수 overnight day에 분산.
- Stop rule: threshold/period 변경, overnight hedge 또는 execution 변경 없음.

## R2-004 — Exposure-normalized Return Attribution

- ID: `R2-004`
- Research question: TSLA dollar contribution이 단위 노출당 return edge, capital scaling 또는 둘 다에서 발생하는가?
- Baseline: Frozen R1-002 10bps.
- Change: 전략 변경 없음. 보유일 return과 notional을 분리 측정.
- Classification: mean overnight +0.10%p/day 및 hit rate +5%p이면 `RETURN_EDGE`; average notional 1.5x이면 `CAPITAL_SCALING`; 둘 다면 `BOTH`.
- Results: TSLA 2019–2020 mean/median overnight return 0.564%/0.629%, hit rate 62.05%, average/median notional $3.21M/$2.24M. Pooled others는 0.285%/0.256%, hit rate 57.06%, notional $0.81M/$0.73M. Mean 차이 +0.279%p, hit-rate 차이 +4.987%p, average notional ratio 3.94x.
- Conclusion: `CAPITAL_SCALING`. Return mean 조건은 통과했으나 hit-rate가 5%p threshold를 0.013%p 하회하여 `RETURN_EDGE`는 부여하지 않음.
- Stop rule: R2 development attribution 종료. Threshold 완화나 sizing/execution 변경 없음.

## R3-000 — S&P 500 PIT Data Feasibility (Pre-registered)

- ID: `R3-000`
- Research question: survivorship-aware/point-in-time S&P 500 universe를 R3 replication에 사용할 만큼 신뢰성 있고 재현 가능하게 확보할 수 있는가?
- Frozen strategy: R1-002 21/63/126, weights 1/1/1, Top 1, 126-day absolute gate, 5-day rebalance, next-open, 10bps.
- Change: 전략 실행 없음. 데이터 공급 범위·품질·접근성 audit만 수행.
- Mandatory gate: PIT membership, delisted securities, permanent identity, corporate actions, delisting treatment, daily open/close, 2014-07~2022 coverage, PIT integrity, immutable snapshot, legal/actual access.
- Go/no-go: 모든 gate와 실제 sample access가 확인돼야 `GO`; 제품은 존재하지만 접근 검증이 없으면 `CONDITIONAL`; 구조적 결손이면 `NO-GO`.
- Final OOS: 봉인.
- Results: 무료 pitindex + Yahoo audit에서 membership 192 snapshots/701 unique tickers/count 498–507을 확인했다. Calibration 후 제한 retry를 포함한 가격 audit 결과는 427/701(60.91%), constituent-date coverage 686,695/1,079,994(63.58%), unresolved 274개였다. Manifest는 검증됐고 Final OOS 행은 0개였다.
- Conclusion: `BLOCKED — DATA QUALITY INSUFFICIENT`. 사전 price 98%, mapping 99%, unresolved 1% 기준을 크게 미달하므로 R3-001을 실행하지 않는다. Threshold 완화, 누락 종목 silent drop, 추가 대규모 retry는 하지 않는다. Final OOS는 봉인한다.

## R3-000C — Final Free-data Clean Retry

- ID: `R3-000C`
- Research question: 기존 60.91% coverage가 implementation/interruption artifact인지 reproducible free-data limitation인지 마지막 1회 독립 확인.
- Setup: 새 `r3_free_sp500_clean_retry_v1`, Python 3.12 ingestion 격리, seed 20260831 previous-missing 30개와 known controls, batch 10, 총 최대 3회, 2/4초 backoff. Final OOS 봉인.
- Calibration results: previous-missing sample 0/30 recovered. 전체 37 requests 중 SUCCESS 3(MSFT/BRK-B/META), invalid payload 9, price not returned 25. Mandatory current control AAPL은 3회 후 invalid payload. Manifest verified, Final OOS flag false.
- Full audit: `NOT RUN`; calibration 선행 gate 실패.
- Conclusion: `BLOCKED`. 기존 저조한 coverage에는 초기 validator bug와 batch/checkpoint artifact가 일부 있었지만 clean sample에서 historical Yahoo availability limitation이 재현됐고 downloader도 mandatory control에서 결정적이지 않았다.
- Stop rule: `R3 CLOSED — BLOCKED BY FREE-DATA QUALITY`. 추가 Yahoo retry/source mixing/manual mapping 없음. R3-001은 current free-data protocol에서 permanently not authorized. R4 plan만 설계하고 performance는 실행하지 않음.

## R4-000 — Fixed-ETF Eligibility and Data-quality Audit (Pre-registered)

- ID: `R4-000`
- Research question: can one liquid, pre-2010, broad ETF per pre-registered economic category be selected from data available by 2014-06-30 without inspecting strategy performance?
- Baseline: frozen R1-002 strategy; it is not executed in R4-000.
- Change: universe construction only. Nine categories and a closed issuer-verified candidate roster are fixed before price inspection.
- Experiment setup: adjusted daily OHLCV for 2013-01-01 through 2014-06-30; 2013 median raw-close dollar volume; USD 5M threshold; maximum-liquidity representative; inception/ticker tie-breaks; common-SPY-calendar coverage audit; Final OOS sealed.
- Success criteria: every category has at least one eligible candidate, selected deterministically, with valid OHLCV, at least 95% date coverage in both audit subperiods, no post-2022 rows, and a reproducible manifest.
- Prohibited: signals, strategy returns, benchmark returns, parameter changes, post-result category/candidate/threshold edits, and R4-001 execution.
- Results: 30/31 candidates returned valid data and had 100% common-SPY-calendar coverage in 2013 and 2014 H1. TLO returned no Yahoo payload and was retained as an explicit failure. Every category had at least one passing candidate. Selected universe: SPY/EFA/EEM/IEF/TLT/LQD/IYR/GLD/DBC. Manifest mismatches 0; post-2022 rows 0; performance outputs 0.
- Conclusion: `ACCEPT` for universe/data-audit feasibility only. This is not a strategy-performance acceptance.
- Next research question: should this immutable universe be authorized for R4-001 replication under the already frozen strategy/evaluation protocol?

## R4A-001 — Frozen Asset-class ETF Replication (Pre-registered)

- ID: `R4A-001` (existing R4-001 scope, renamed only to distinguish R4B)
- Hypothesis: frozen R1-002 can preserve risk-adjusted benchmark value while reducing single-name and temporal concentration across nine independently selected macro asset ETFs.
- Baseline: frozen R1-002 parameters; no alpha or parameter change.
- Change: universe only, from ex-post AMD/TSLA/AMZN/AAPL to frozen SPY/EFA/EEM/IEF/TLT/LQD/IYR/GLD/DBC.
- Experiment setup: 2015–2022 development, warm-up from 2014-07, next-open, 0/5/10/20bps, SPY and universe equal-weight benchmarks. Final OOS sealed.
- Decision criteria: fixed in `R4_PLAN.md` before development prices or performance are inspected.
- Results: snapshot 9/9 symbols, 2,142 common dates, 2014-07-01 through 2022-12-30, post-OOS rows 0. At 10bps total return 11.68%, CAGR 1.39%, Sharpe 0.167, Sortino 0.201, Calmar 0.045, MDD -31.05%, turnover 217.91x and 227 trades. SPY return 115.50%; equal-weight return 33.37%. Maximum ETF concentration 26.62% (EEM), 8 sold assets, non-equity positive P&L, positive 2-year blocks 2/4. 0bps return 40.13%, 20bps -10.99%.
- Conclusion: `REJECT`. Concentration generalized favorably, but return/risk-adjusted benchmark performance and temporal/cost robustness failed the frozen criteria.
- Next research question: can R4B-000 obtain a survivorship-aware, exposure-deduplicated historical ETF master without repeating R3's silent survivorship/data-quality failure?

## R4B-000 — Broad ETF Data Feasibility (Design Only)

- ID: `R4B-000`
- Research question: can a survivorship-aware, exposure-deduplicated broad ETF universe be reconstructed as of 2014-06-30 with sufficient next-open and liquidation coverage?
- Frozen strategy: R1-002 unchanged; performance prohibited.
- Results: official-source review found CRSP survivor-bias-free fund data structurally suitable but subscription-only and unavailable to the project. Nasdaq's public symbol directory is current-day; its historical Daily List is a corporate-action supplement, not a complete exposure-classified ETF master with adjusted prices and liquidation proceeds.
- Conclusion: `CONDITIONAL — DATA EXISTS, ACCESS NOT VERIFIED`; R4B-001 `NOT AUTHORIZED`.
- Next research question: whether to obtain licensed CRSP-equivalent access for sample validation or close R4B without performance.

## R4B-000F — Free-data-only Final Feasibility Audit

- ID: `R4B-000F`
- Decision constraint: free sources only; no licensed CRSP/Nasdaq product.
- Research question: can official free sources jointly reconstruct the frozen 2014 broad ETF master with measurable completeness, stable identity, exposure deduplication, inactive funds, adjusted prices and terminal treatment?
- Evidence: SEC EDGAR offers free filing archives/submissions metadata but no integrated 2014 ETF master/trading/terminal schema; structured N-CEN/N-PORT history begins after the freeze date. Nasdaq historical Daily List is subscription-only. Current directories and Yahoo cannot measure missing inactive funds.
- Results: mandatory master, inactive-fund completeness, ticker-effective-history, exposure and terminal-price gates cannot all be verified under the free-only constraint.
- Conclusion: `BLOCKED — FREE-DATA COVERAGE INSUFFICIENT`; R4B-001 `NOT AUTHORIZED`.
- Stop rule: no more free-source stitching, survivor-only performance, threshold relaxation or manual mapping. Reopen only under a new licensed-data decision.

## S1-001 — R1–R4 Evidence Synthesis

- ID: `S1-001`
- Research question: after dependency audits, independent replication and data-quality gates, what evidence remains for R1-002 and should it consume Final OOS or continue as an active candidate?
- Evidence: R1 local development improvement; R2 TSLA/payoff/period/capital-scaling dependence; R4A 10bps CAGR 1.39%, Sharpe 0.167 and benchmark underperformance despite lower 26.62% concentration; R3/R4B data-blocked with no performance.
- Results: evidence for a universal momentum/risk-off edge is materially weakened. The original development phenomenon remains documented but is not independently replicated.
- Conclusion: `REJECT AS ACTIVE GENERAL STRATEGY CANDIDATE`; preserve frozen historical code/results and stop adjacent tuning.
- Final OOS: remain SEALED; do not spend it on the weakened candidate.
- Next research question: R5-000 should compare genuinely new strategy families, data requirements and falsification tests before any performance run.

## R5-000 — New Strategy Research Design

- ID: `R5-000`
- Research question: which genuinely new strategy family best addresses the empirical and data failures found in R1–R4?
- Candidates: independent time-series trend plus risk allocation; cross-sectional momentum; pure multi-asset risk allocation.
- Setup: design and local metadata feasibility only. No price download, signal, return, benchmark or performance calculation.
- Result: recommend long-or-cash independent trend with unlevered risk-based allocation. Pure inverse volatility is retained as a structural baseline; cross-sectional momentum is deprioritized because it repeats ranking and concentration risks.
- Proposed data protocol: frozen SPY/EFA/EEM/IEF/TLT/LQD/IYR/GLD/DBC universe; 2006 warm-up; 2007–2014 development subject to a new data-only gate. 2015–2022 is contaminated research history, not clean validation.
- Conclusion: `DESIGN COMPLETE — SECOND OPINION REQUIRED`.
- Authorization: R5-001 not authorized before approval of family, period, universe, canonical parameter sources and quantitative decision thresholds.
- Final OOS: 2023–2025 remains SEALED.

### Option A approval

- User approved the recommended Option A family.
- A single canonical implementation proposal was registered before performance: 12-month own-return sign, monthly next-open execution and 60-day-center-of-mass EWMA inverse-volatility allocation, long/cash and unlevered.
- Quantitative risk-adjusted, benchmark, period/name concentration and 20bps cost gates were added before any R5 result.
- R5-001 remains not authorized until exact-protocol confirmation and the 2006–2014 data-only gate pass.

## R5-001 — Independent Trend with Risk-based Allocation

- ID: `R5-001`
- Hypothesis: independent 12-month trend plus unlevered inverse-volatility allocation improves risk-adjusted performance and concentration relative to pure risk allocation and equal-weight trend.
- Baseline: inverse-volatility/no-trend and equal-weight independent trend; passive SPY and universe equal-weight context.
- Setup: frozen nine ETFs, 2007-03-01–2014-12-31, month-end close/next-open, EWMA decay 60/61, 0/5/10/20bps, no leverage or shorting. Final OOS sealed.
- Data gate: 9/9 symbols, 99.9554% minimum common-calendar coverage, latest row 2014-12-31, manifest verified.
- Results: at 10bps total return 72.29%, CAGR 7.19%, volatility 8.04%, MDD -12.66%, Sharpe 0.905, Sortino 1.254, Calmar 0.568 and turnover 21.90x. Inverse-vol/no-trend Sharpe 0.742 and Calmar 0.262; equal-weight trend Sharpe 0.762 and Calmar 0.408. SPY CAGR was slightly higher at 7.34%.
- Dependency: 4/4 positive two-year blocks; maximum block contribution 27.33%; maximum asset contribution 19.22%; 20bps result remained positive.
- Conclusion: `ACCEPT — DEVELOPMENT EVIDENCE ONLY`; all frozen checks passed, but this is not final candidate selection.
- Next: bounded R5-002 robustness without adjacent parameter search. Final OOS remains SEALED.

## R5-002 — Frozen-rule Contaminated Period Stress

- ID: `R5-002`
- Question: does the unchanged R5-001 rule preserve its direction in the already-observed 2015–2022 period without tuning?
- Classification: `RESEARCHER_CONTAMINATED_STRESS_DIAGNOSTIC`; not clean OOS.
- Setup: same universe, signals, weights, timing and 0/5/10/20bps; no parameter change. Final OOS sealed.
- Results: at 10bps total return -0.87%, CAGR -0.11%, MDD -22.10%, Sharpe 0.037, Calmar -0.005 and turnover 30.16x. Inverse-vol/no-trend Sharpe was 0.403; equal-weight trend Sharpe 0.131. Only 1/4 two-year blocks was positive.
- Cost: total return +2.24%/0.70%/-0.87%/-3.85% at 0/5/10/20bps.
- Conclusion: `REJECT — STRONG PERIOD INSTABILITY`.
- Decision boundary: conflicts with R5-001 development ACCEPT. Stop R5-003, tuning and candidate promotion; request second opinion. Final OOS remains SEALED.

## R5-003 — Bounded Failure Attribution and Literature Review

- ID: `R5-003`
- Question: why did the unchanged trend plus risk-allocation rule vary so strongly across the two historical periods?
- Scope: descriptive decomposition only; signal, allocation, turnover, asset, period and cost. No strategy or parameter change.
- Signal evidence: positive-signal mean payoff fell 0.646% to 0.305%; negative-signal assets subsequently rose 0.235% versus 0.576%; overall hit rate fell 54.48% to 51.70%.
- Allocation evidence: candidate-minus-no-trend Sharpe changed from +0.163 to -0.366; candidate-minus-equal-trend Sharpe from +0.143 to -0.094.
- Whipsaw/cost: transitions rose 78 to 90 but false-transition rate fell 53.85% to 47.78%; 0-to-10bps drag was 3.83%p versus 3.11%p. Neither is the primary explanation.
- Asset/period: early contributions were positive across groups; later equity and real assets were negative. Early success was not concentrated in the NBER GFC recession window; the COVID recession window was negative.
- Conclusion: `DIRECTIONAL PAYOFF DETERIORATION + ALLOCATION EFFECT REVERSAL`; moderate descriptive confidence, low causal confidence.
- Literature: broad instability, reversal and scaling effects are substantially known. The potential gap is a unified component-level structural-break design under matched exposure.
- R5 closure: no final strategy; no tuning; Final OOS remains SEALED.

## Experiment Template

- ID:
- Hypothesis:
- Baseline:
- Change:
- Experiment setup:
- Results:
- Conclusion: `ACCEPT` / `REJECT` / `INCONCLUSIVE`
- Next research question:

## ALPHA-LAB-v1 — Research Infrastructure Design

- ID: `ALPHA-LAB-v1`
- Objective: establish a governed discovery system capable of testing many cross-sectional alpha hypotheses without silent data mining.
- Change: documentation and research metadata architecture only; no production alpha engine or performance test.
- Outputs: WorldQuant public-model audit, alpha protocol/catalog/families, data and universe feasibility, temporal governance, metrics/inference, multiple-testing policy, paper bridge and proposed A001–A010 calibration batch.
- Data conclusion: free current-member histories are not survivorship-free; recommend survivorship-limited historical discovery plus a prospectively maintained broad-universe shadow registry.
- Temporal conclusion: 2007–2022 contaminated; 2023–2025 Final OOS SEALED; future prospective cohorts provide clean validation.
- Status: `DESIGN COMPLETE — FREEZE DECISION PENDING`.
- Results: no alpha performance, backtest, parameter optimization or data download.
- Next decision: freeze Alpha Lab v1 architecture and implement the minimum data/ledger/evaluation engine, modify the protocol, or stop.
