# Research Principles

이 문서는 repository의 지속적인 quant research 운영 원칙을 기록한다. `AGENTS.md`의 안전·백테스트 원칙을 보완하며, 충돌할 경우 더 엄격한 안전 원칙을 따른다.

## Research Objective

- 현재 목표는 live performance를 주장하는 것이 아니라 재현 가능하고 편향을 명시한 research process를 구축하는 것이다.
- P1 research-ready backtester를 기준 도구로 사용하며, 전략 수익률 극대화보다 검증 가능한 가설과 올바른 비교를 우선한다.
- R1의 고정 primary baseline은 Cross-sectional Momentum Rotation이다. R1-002는 현재 development 단계 candidate이며 최종 채택 전략이 아니다.

## Experimental Discipline

- 한 iteration에는 하나의 독립적인 research question과 하나의 주요 변경만 둔다.
- 구현과 결과 조회 전에 hypothesis, rationale, baseline, fixed setup, success/failure criteria를 사전 등록한다.
- 실패한 실험도 `RESEARCH_LOG.md`에 기록하며 결과를 본 뒤 가설이나 판정 기준을 소급 변경하지 않는다.
- ACCEPT는 단순 total return 증가만으로 결정하지 않는다. CAGR, volatility, MDD, Sharpe, Sortino, Calmar, turnover, 거래 수, benchmark excess return과 필요한 concentration 진단을 함께 본다.
- neighboring parameter를 결과 확인 후 연속 탐색하지 않는다. Parameter search가 필요하면 범위와 평가 방법을 먼저 고정한다.
- Development 결과를 본 뒤 primary baseline을 소급 변경하지 않는다.

## Fixed R1 Protocol

- Development: 2015-01-01–2022-12-31
- Final untouched OOS: 2023-01-01–2025-12-31
- Primary universe: AMD, TSLA, AMZN, AAPL
- SPXL: primary에서 제외하고 별도 robustness에만 사용
- Primary benchmark: SPY adjusted buy-and-hold
- Secondary benchmark: universe equal-weight buy-and-hold
- Initial cash: USD 100,000
- Primary execution cost: commission 0bps, one-way slippage 10bps
- Cost robustness: one-way slippage 0/5/10/20bps
- Signal/execution: close로 생성한 signal은 다음 거래일 open에 체결
- Data: frozen local Yahoo/yfinance adjusted development snapshot. Final OOS는 현재 다운로드하지 않음.

## Bias and Interpretation

- 현재 universe는 ex-post selected이므로 selection 및 survivorship bias 가능성을 모든 결과에 명시한다.
- Yahoo/yfinance 데이터는 institutional-grade point-in-time dataset으로 간주하지 않는다.
- 정적 ROE/PBR 사용 결과는 `BIASED_RESEARCH_MODE`로 표시하며 point-in-time fundamentals 검증으로 해석하지 않는다.
- 거래원장 기반 realized-P&L concentration은 완전한 portfolio return attribution이 아님을 표시한다.
- 고정 bps 비용 모델은 spread, market impact, tax와 FX를 완전히 반영하지 않는다.

## Autonomous Decisions

Quant Research Engineer는 다음 routine decision을 자율적으로 수행할 수 있다.

- 다음 단일 factor hypothesis의 우선순위 선정
- 기존 protocol 안에서의 최소 구현과 synthetic/unit test
- 사전 기준에 따른 `ACCEPT`, `REJECT`, `INCONCLUSIVE` 판정
- 결과가 명확할 때 다음 독립 실험의 제안과 설계

다음 high-impact decision에는 SECOND OPINION을 요청한다.

- Final OOS 개봉
- Baseline 또는 연구 protocol의 사후 변경
- Parameter search 범위 확대
- 서로 충돌하는 강한 증거의 해석
- 새로운 외부 데이터 또는 ML 방법론 도입
- 최종 candidate 선정
- Paper trading 또는 live trading 전환

## Safety and Reproducibility

- 실제 broker API, token 발급 또는 live order는 research workflow에서 호출하지 않는다.
- 연구 test는 local snapshot과 synthetic/mock data만 사용한다.
- Snapshot provenance, 날짜 범위와 hash를 검증한다.
- 실행 코드와 보고서에는 Final OOS seal 여부와 주요 bias warning을 유지한다.
- Commit과 push는 사용자의 명시적 요청 없이 수행하지 않는다.

## Bounded Development Batch R1-005–R1-007

- 2026-08-30 second opinion으로 세 개의 독립 가설을 결과 조회 전에 일괄 사전등록하는 Option A를 승인했다.
- 세 실험은 R1-002에 각각 독립 적용하며 서로 누적하지 않는다.
- 중간에 ACCEPT가 발생해도 나머지 실험을 생략하거나 변경하지 않는다.
- 세 실험 완료 후 ACCEPT 유무와 관계없이 이 development batch를 종료한다.
- 공통 ACCEPT 기준: 10bps에서 Sharpe/Sortino/Calmar 중 최소 2개가 개선되고 어느 것도 0.05를 초과해 악화되지 않으며, MDD 악화가 3%p 이내, CAGR이 R1-002의 80% 이상, 두 benchmark 대비 excess return이 양수, turnover 증가가 20% 이내여야 한다. 비용별 방향이 심하게 충돌하면 INCONCLUSIVE다.
- Concentration과 2년 구간 성과는 필수 diagnostic이며 결과를 본 뒤 공통 기준을 변경하지 않는다.

## Final OOS Double Confirmation

- Final OOS 개봉을 암시하는 일반 요청은 허가로 간주하지 않는다.
- 사용자가 `2023–2025 Final OOS를 개봉하라`고 명시적으로 요청해야 한다.
- 첫 요청 후 Quant Research Engineer는 개봉 범위와 비가역성을 설명하고 반드시 두 번째 명시적 확인을 받는다.
- 두 번째 확인 전에는 Final OOS를 다운로드, 조회, 계산 또는 보고하지 않는다.

## R1 Closure

- R1은 R1-007 bounded batch 완료 시점에 종료한다.
- R1-001은 frozen primary baseline, R1-002는 frozen development candidate다.
- R1의 기존 parameter와 판정은 소급 변경하지 않는다.
- R2는 새로운 alpha tuning보다 robustness와 dependency audit를 우선한다.
