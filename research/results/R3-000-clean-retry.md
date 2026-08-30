# R3-000 — Final Free-data Clean Retry

## Decision

`BLOCKED AT CALIBRATION — DATA INGESTION NOT AUDIT-READY`

이 clean retry는 마지막 무료 S&P 500 attempt다. Calibration gate 실패로 701-ticker full audit은 실행하지 않았고 R3-001 performance도 실행하지 않았다.

## Isolation and Protocol

- Snapshot ID: `r3_free_sp500_clean_retry_v1`
- Historical attempt `r3_free_sp500_v1_audit2`와 파일을 혼합하지 않음
- Python 3.12.7 ingestion / Python 3.9.6 research·broker runtime 분리
- pitindex 0.2.1 bundled membership; 192 snapshots, 701 unique tickers, count 498–507
- Yahoo/yfinance 1.7.0 adjusted OHLCV
- Download boundary: 2014-07-01 inclusive, 2023-01-01 exclusive
- Batch 10, 총 최대 3회, 2초/4초 backoff
- Seed 20260831로 기존 unresolved 30개를 결과 조회 전에 고정

## Calibration Result

- Deterministic previous-missing sample: 0/30 recovered
- All unique calibration/control requests: 37
- `SUCCESS`: 3 (MSFT, BRK-B, META)
- `invalid_price_payload`: 9
- `price_not_returned`: 25
- Mandatory current control AAPL: 3회 후 `invalid_price_payload`
- Known merger/delisted/unavailable controls CELG, ALXN, FTR, BRCM, PETM: price not returned
- Final OOS rows/download flag: 0 / false
- Calibration manifest: verified

## Adjudication

Calibration은 downloader/validator가 audit-ready해야 한다는 선행 gate를 실패했다. 특히 기존 missing 표본의 회복이 0%였고 정상 control AAPL도 안정적으로 처리하지 못했다. 따라서 full audit을 강행하지 않았다.

기존 60.91% 결과의 원인은 하나가 아니다.

1. 최초 4.1%는 R1 validator를 잘못 재사용한 implementation defect였다.
2. 기존 공식 attempt는 checkpoint 부재와 batch/payload instability 영향을 받았다.
3. Clean calibration에서 과거 종목 30개가 하나도 회복되지 않아 Yahoo의 historical/delisted availability limitation도 재현됐다.
4. AAPL control 실패는 무료 downloader/payload가 동일 protocol에서 완전히 결정적이지 않음을 보여준다.

Engineering artifact가 일부 있었지만 이를 제거해도 mandatory 98%/99%/1% gate를 신뢰성 있게 검증할 수 없다. Threshold를 완화하거나 특정 ticker만 추가 retry하지 않는다.

## Final Status

`R3 CLOSED — BLOCKED BY FREE-DATA QUALITY`

- R3-001: permanently `NOT AUTHORIZED` under the current free-data protocol
- Reopen condition: 새로운 institutional/PIT dataset을 확보하고 별도의 high-impact research decision을 내릴 때만 가능
- Frozen R1-002: unchanged
- Final OOS 2023–2025: SEALED
