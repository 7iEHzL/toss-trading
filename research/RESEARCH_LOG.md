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
- Experiment setup: 코드로 고정 완료. Adjusted local snapshot 대기 중.
- Results: `PENDING_DATA`; final OOS 미조회.
- Conclusion: `INCONCLUSIVE`
- Next research question: 로컬 adjusted snapshot 확보 후 development 및 walk-forward 평가.

## Experiment Template

- ID:
- Hypothesis:
- Baseline:
- Change:
- Experiment setup:
- Results:
- Conclusion: `ACCEPT` / `REJECT` / `INCONCLUSIVE`
- Next research question:
