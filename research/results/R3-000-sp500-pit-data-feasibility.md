# R3-000 — S&P 500 Point-in-Time Data Feasibility

## Decision

`CONDITIONAL — R3-001 NOT AUTHORIZED`

신뢰할 수 있는 상용 데이터 조합은 존재하지만, 현재 프로젝트에는 해당 라이선스·접근권한·검증된 샘플이 없다. 따라서 제품 설명만으로 품질 gate를 통과한 것으로 간주하지 않으며 R3-001 replication은 시작하지 않는다.

## Pre-registered Scope

- 데이터 확보 가능성만 조사한다. 전략 수익률은 계산하지 않는다.
- R1-002의 21/63/126, 동일 가중 score, Top 1, 126-day absolute-momentum gate, 5-day rebalance, next-open, 10bps를 동결한다.
- Top N, lookback, weight, rebalance parameter를 탐색하지 않는다.
- Final OOS 2023–2025는 다운로드·조회하지 않는다.
- R3의 목적은 CAGR 재현이 아니라 종목·기간·regime 일반화와 concentration 감소 여부 검증이다.

## Candidate Data Stacks

| Candidate | Officially documented strengths | Unverified or missing for this project | Verdict |
|---|---|---|---|
| Norgate Data US Stocks Platinum/Diamond | Historical S&P 500 constituents, delisted securities, daily open/close, corporate-event fields, Windows Python access | 실제 구독/시험판 접근, 샘플 스키마, 영구 식별자 운용, delisting terminal-value 규칙, snapshot 고정 절차를 검증하지 않음 | `CONDITIONAL` |
| S&P SPICE + CRSP US Stock | SPICE의 공식 historical constituents/add-drop history; CRSP의 PERMNO, daily open/close, distributions 및 delisting-return 계열 필드 | 두 라이선스 모두 현재 없음; 양쪽 식별자 매핑, 유효일 의미, export 재현성을 샘플로 검증하지 않음 | `CONDITIONAL` |
| 현재 Yahoo/yfinance snapshot | 기존 개발 실험을 재현하는 로컬 스냅샷과 OHLC | PIT membership, 삭제 종목 전체, permanent ID, delisting return, 공급자 vintage를 충족하지 못함 | `NO-GO` |

## Mandatory Gate Assessment

| Gate | Current status | Reason |
|---|---|---|
| PIT S&P 500 membership/effective dates | 미충족 | 공식 상용 제품의 제공 가능성만 확인; 실제 row-level sample 미검증 |
| Survivorship awareness | 미충족 | 현재 데이터에는 historical exits/delisted universe가 없음 |
| Stable security identity | 미충족 | 현재 pipeline은 ticker 중심이며 permanent-ID mapping 없음 |
| Corporate actions | 미검증 | 상용 후보의 기능은 확인했으나 전략 입력으로의 조정 규칙 미검증 |
| Delisting treatment | 미충족 | terminal value/delisting return 적용 규칙과 샘플 없음 |
| Daily open/close and trading status | 부분 충족 | 후보 제품은 OHLC를 제공하지만 결측·halt·next-open 규칙 미검증 |
| 2014-07 through 2022 coverage | 제품상 가능 | 실제 constituent-price join 및 warm-up completeness 미검증 |
| PIT/vintage integrity | 미검증 | provider correction과 snapshot as-of 정책을 아직 고정하지 못함 |
| Immutable reproducible snapshot | 미충족 | licensed export와 manifest/hash 생성 전 |
| Legal and operational access | 미충족 | 현재 라이선스·계정·승인된 export가 없음 |

`GO`는 열 가지 gate 전부와 실제 샘플을 검증해야 한다. 현재는 구조적으로 불가능한 것은 아니지만 실제 접근 검증이 없으므로 `CONDITIONAL`이다.

## Minimum Sample Audit Before R3-001

데이터를 확보하더라도 즉시 백테스트하지 않는다. 먼저 별도 audit에서 다음을 확인한다.

1. 임의 날짜의 membership가 effective date 기준으로 재구성되는지 확인한다.
2. 기간 중 편입·편출·ticker 변경·합병·상장폐지 사례를 permanent ID로 추적한다.
3. raw/adjusted open-close, split, dividend, delisting 처리를 수작업 검산한다.
4. membership와 price join에서 누락률, 중복, 비거래일, 첫 거래 가능 open을 검사한다.
5. source/version/as-of, schema, row counts, file hashes를 manifest에 고정한다.
6. 라이선스가 로컬 연구 snapshot 저장과 재현 가능한 export를 허용하는지 확인한다.

이 audit가 모두 통과해야 별도 사전등록된 R3-001을 시작할 수 있다.

## Sources Reviewed

- Norgate Data Accessibility: historical index constituents, survivorship-bias support, delisted-security subscription requirement, Windows Python access.
- Norgate Data Content Tables: US daily open/close definitions, delisted coverage, historical constituents and capital-event fields.
- S&P DJI SPICE: S&P 500 constituent history from 1964, adds/drops from 1989, constituent/corporate-action downloads.
- CRSP US Stock documentation: permanent security identifier, daily open/close, distributions and delisting data fields.

## Conclusion

R3-000은 데이터가 존재하지 않는다는 `NO-GO`가 아니라, 현재 접근권한과 row-level 검증이 없는 `CONDITIONAL`이다. 무료 현재-구성종목/yfinance 방식으로 결과를 억지로 만들지 않는다. 다음 단계는 licensed-data sample audit를 승인받거나, 별도의 high-impact 결정으로 Option B를 선택하는 것이다.
