# R3 Independent Universe Replication Plan

## Status

`R3 CLOSED — BLOCKED BY FREE-DATA QUALITY; R3-001 PERMANENTLY NOT AUTHORIZED UNDER CURRENT PROTOCOL`

## Objective

R3는 frozen R1-002가 survivorship-aware, point-in-time S&P 500 universe에서 종목·기간·regime에 걸쳐 일반화되는지와 single-name concentration이 감소하는지를 검증한다. CAGR 재현이나 parameter optimization이 목적이 아니다.

## Frozen Strategy Protocol

- Relative momentum lookbacks: 21/63/126 trading days
- Relative momentum weights: 1/1/1
- Selection: Top 1
- Risk-off: selected winner의 126-day absolute momentum이 `<= 0`이면 cash
- Rebalance: every 5 trading days
- Signal/execution: close signal, next trading-day open
- Primary execution cost: commission 0bps, one-way slippage 10bps
- Cost robustness: 0/5/10/20bps
- No search: Top N, lookback, weight, rebalance interval 또는 gate threshold 변경 금지
- Final OOS 2023–2025: double-confirmation seal 유지

## R3-000 — S&P 500 PIT Data Feasibility Audit

R3-000에서는 전략을 실행하거나 성과를 계산하지 않는다. 공식 공급자 문서와 실제 접근 가능성을 확인하고 아래 gate를 모두 충족할 때만 R3-001을 허용한다.

### Mandatory Data Quality Gate

1. Point-in-time S&P 500 membership
   - 각 구성종목의 실제 편입·편출 effective date 제공
   - 임의 날짜에 당시 투자 가능 universe를 재구성 가능
2. Survivorship awareness
   - 편출·상장폐지·합병 종목 포함
   - 현재 ticker 목록만으로 과거를 재구성하지 않음
3. Stable security identity
   - ticker 변경과 재사용을 구분할 permanent identifier 또는 검증 가능한 mapping
4. Corporate actions
   - split, dividend, merger와 spin-off를 일관되게 처리할 가격·조정 정보
5. Delisting treatment
   - 상장폐지일과 가능한 경우 delisting return/terminal value 제공
   - 부재 시 손실 처리 규칙을 사전 정의할 수 있는 충분한 status 정보
6. Price fields and timing
   - 일별 open/close 및 거래일 calendar
   - next-open execution에 필요한 누락·정지·비거래 상태 식별 가능
7. Coverage and warm-up
   - 최소 2014-07-01부터 2022-12-31까지 membership과 price coverage
   - 2015 evaluation 이전 126 trading-day warm-up 확보
8. Point-in-time integrity
   - 데이터 공개/수정 시각 또는 vintage 특성을 확인할 수 있어 사후 수정 정보를 신호 시점에 사용하지 않음
9. Reproducibility
   - 허용된 방식으로 로컬 immutable snapshot 생성 가능
   - source version/as-of, row counts, hashes와 provenance 기록 가능
10. Legal and operational access
   - 프로젝트에서 사용할 수 있는 라이선스와 실제 접근권한 보유
   - Python 또는 재현 가능한 export workflow 제공

### Go/No-go Rule

- `GO`: 열 가지 mandatory gate가 모두 충족되고 실제 접근권한과 sample schema를 검증함.
- `CONDITIONAL`: 공식 제품은 gate를 충족할 가능성이 높지만 현재 라이선스·접근권한·sample 검증이 없음.
- `NO-GO`: membership, delisting, identity 또는 next-open price 중 하나라도 구조적으로 충족하지 못함.

`CONDITIONAL` 또는 `NO-GO`에서는 R3-001을 실행하지 않는다. Option B ETF universe 전환은 별도 high-impact decision으로 다시 판단한다.

## R3-001 — Replication Gate

R3-000이 `GO`일 때만 별도로 사전등록한다. Universe 정의, evaluation blocks, benchmark, missing-price와 delisting 처리 규칙을 데이터 schema 확인 후 결과 조회 전에 고정한다.

## Free-data Quality Thresholds (Pre-registered Before Download)

- Development download boundary: `start >= 2014-07-01`, `end exclusive = 2023-01-01`; 2023년 이후 행은 0개여야 한다.
- PIT membership size: 각 관측 snapshot에서 480–520 securities.
- Duplicate `(as_of, ticker)`: 0개.
- Membership date leakage: 요청일 이후 effective state 사용 0건.
- Price coverage: membership 요청 종목 중 유효 OHLC가 있는 종목 98% 이상.
- Mapping resolution: `exact` 또는 근거가 기록된 `mapped` 상태 99% 이상; `unresolved` 1% 이하.
- Price integrity: duplicate date, missing OHLC, non-finite/non-positive OHLC, OHLC inconsistency 각각 0건.
- Warm-up: 첫 evaluation date 이전 최소 126 trading days.
- Secondary membership mismatch: 신뢰 가능한 무료 cross-check가 확보된 날짜에서 symmetric difference 2% 이하. Secondary source가 없으면 통과로 간주하지 않고 전체 판정을 최대 `CONDITIONAL`로 제한한다.
- Reproducibility: metadata 필수 필드 누락 0개, manifest SHA-256 mismatch 0개.
- Free-data disclosure: `FREE_DATA_REPLICATION_MODE=True`, `survivorship_free=False`, `delisted_coverage_complete=False`, `final_oos_downloaded=False`를 강제한다.

Threshold는 coverage나 성과 결과를 본 뒤 완화하지 않는다. Price coverage, PIT integrity, hash verification 중 하나라도 실패하면 `BLOCKED`; threshold는 통과하지만 secondary cross-check 또는 delisting completeness가 미검증이면 `CONDITIONAL — LIMITED REPLICATION ONLY`; 모든 무료-data gate가 충족된 경우에만 `PASS — FREE-DATA REPLICATION AUTHORIZED` 후보가 된다.

## R3-000 Clean Retry — Final Free-data Attempt (Pre-registered)

- Snapshot ID: `r3_free_sp500_clean_retry_v1`
- Purpose: 기존 60.91% 결과가 engineering artifact인지 실제 reproducible free-data limitation인지 독립 확인한다.
- Attempts: clean retry는 정확히 1회이며 중단 시 checkpoint의 unfinished 항목만 resume한다. 완료 후 추가 Yahoo retry는 금지한다.
- Environment: Python 3.12 ingestion과 Python 3.9 broker/research runtime을 분리한다.
- Price boundary: 2014-07-01 inclusive, 2023-01-01 exclusive.
- Retry policy: initial batch 10 symbols; 실패 시 single-symbol 최대 2회 추가 시도(총 최대 3회), 2초와 4초 exponential backoff. `SUCCESS` checkpoint는 다시 요청하지 않는다.
- Calibration seed: `20260831`.
- Deterministic unresolved sample (30): AIV, BCR, BEN, CA, CELG, CFN, CMCSK, CPB, DWDP, FDX, FTR, HES, JOY, K, LLL, LMT, LVLT, MMC, PDCO, PKI, PRGO, RDC, RE, RF, SIAL, STJ, TEG, TSS, WBA, WMB.
- Known controls: current AAPL/MSFT; punctuation BRK.B→BRK-B; rename FB→META; merger CELG/ALXN; delisted FTR; suspected unavailable BRCM/PETM. Known labels are audit expectations only이며 price 결과에 따라 새 mapping을 만들지 않는다.
- Calibration gate: current/punctuation controls가 batch 또는 제한 single verification으로 유효 OHLC를 반환하고, 모든 request가 2023-01-01 exclusive를 지켜야 한다. Safety/validator/checkpoint defect가 있으면 full audit 전에 수정·재검증한다.
- Error taxonomy: `SUCCESS`, `TEMPORARY_FAILURE`, `RATE_LIMITED`, `TIMEOUT`, `BATCH_FAILURE_SINGLE_SUCCESS`, `SYMBOL_FORMATTING`, `TICKER_RENAME`, `MERGER_ACQUISITION`, `DELISTED_SECURITY`, `NO_HISTORICAL_DATA`, `AMBIGUOUS_IDENTITY`, `INVALID_MEMBERSHIP_RECORD`, `UNRESOLVED`.
- Full audit gate: 기존 98% price, 99% mapping, unresolved 1%, OHLC 0-error, Final OOS 0-row, hash 0-mismatch 기준을 그대로 사용한다.
- Additional diagnostics: constituent-date coverage, signal/rebalance-date tradable coverage, 126-day warm-up availability, next-open availability, missing constituent-day concentration, delisted/merger subgroup coverage. 결과를 본 뒤 새 PASS threshold를 만들지 않는다.
- PASS/CONDITIONAL: R3-001 authorization candidate로만 변경하고 성과를 실행하지 않는다.
- BLOCKED: `R3 CLOSED — BLOCKED BY FREE-DATA QUALITY`; R3-001 permanently not authorized unless a new institutional/PIT dataset decision reopens it. R3 code를 KEEP/GENERALIZE/ARCHIVE/REMOVE로 분류하고 R4 계획만 작성한다.
