# R3-000 — Free-data S&P 500 PIT Audit

## Decision

`BLOCKED — DATA QUALITY INSUFFICIENT`

R3-001 performance replication은 실행하지 않는다. Final OOS 2023–2025는 봉인 상태다.

## Scope

- Membership: `pitindex 0.2.1` bundled S&P 500 reconstruction
- Price: Yahoo Finance via `yfinance 1.7.0`, adjusted OHLCV
- Download boundary: 2014-07-01 inclusive through 2023-01-01 exclusive
- Strategy execution: 없음
- Frozen R1-002 parameter 변경: 없음

## Environment and Membership

- Data-ingestion runtime: Python 3.12.7, broker/research 기본 Python 3.9와 분리
- Membership snapshots: 192
- Unique PIT tickers: 701
- Snapshot constituent count: 498–507
- Bundle age at audit: 48 days; historical integrity와 current freshness는 별도 문제로 취급
- Secondary membership cross-check: 없음

## Calibration

전체 audit 전에 AAPL, MSFT, SPY, BRK-B를 batch와 single-symbol 방식으로 비교했다. 첫 실행에서 AAPL 응답이 일시적으로 실패했으나 동일한 전체 calibration을 사전 선언한 마지막 1회 재실행했고, 네 종목 모두 2,142행과 동일한 날짜 범위로 통과했다. 2023년 이후 행은 없었다.

## Actual Audit Results

| Metric | Pre-registered gate | Result | Status |
|---|---:|---:|---|
| PIT constituent count | 480–520 | 498–507 | PASS |
| Unique ticker price coverage | >=98% | 60.91% (427/701) | FAIL |
| Mapping resolution | >=99% | 60.91% | FAIL |
| Unresolved tickers | <=1% | 274/701 (39.09%) | FAIL |
| Constituent-date coverage | diagnostic | 63.58% (686,695/1,079,994) | INSUFFICIENT |
| Final OOS rows | 0 | 0 | PASS |
| Manifest hash mismatch | 0 | 0 | PASS |
| Secondary mismatch | <=2% when available | not available | UNVERIFIED |

Yahoo의 batch 누락에는 제한된 single-symbol retry를 적용했다. 그래도 과거·현행 ticker가 함께 대량 실패했으므로 Yahoo 메시지를 근거로 상장폐지를 자동 판정하지 않았다. 실패는 unresolved price/identity coverage로 유지했다.

## Research Interpretation

- 이 결과는 frozen R1-002의 성과 실패가 아니라 데이터 pipeline quality gate 실패다.
- 60.91% ticker coverage와 63.58% constituent-date coverage에서는 누락 종목을 조용히 제외한 replication을 수행할 수 없다.
- 무료 source를 계속 혼합하거나 수동 mapping을 대량 추가하면 새로운 identity·corporate-action 오류와 선택 편향이 생긴다.
- Threshold를 사후 완화하지 않는다.
- `FREE_DATA_REPLICATION_MODE=True`, `survivorship_free=False`, `delisted_coverage_complete=False`, `final_oos_downloaded=False`를 유지한다.

## Stop Rule

현재 pitindex + Yahoo 무료 S&P 500 경로는 종료한다. R3-001은 승인하지 않는다. Fixed ETF universe 같은 별도 independent study로 전환하려면 새로운 연구 질문과 protocol을 사전등록하는 high-impact decision이 필요하다.
