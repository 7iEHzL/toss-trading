# R3 Code and Artifact Cleanup

R3 free-data 실패 기록은 보존하면서 active codebase의 일회성 실행 코드는 정리한다.

## KEEP

- `research/R3_PLAN.md`, `research/results/R3-000-*.md`, `research/RESEARCH_LOG.md`, `research/DECISIONS.md`: 연구 protocol, 실패 증거와 의사결정 history.
- `requirements-r3-ingestion.txt`: broker Python 3.9와 ingestion Python 3.11+를 분리하는 재현성 계약.
- `data/sources/yahoo_price_source.py`: OOS boundary, adjusted OHLC validation과 제한 retry가 있는 일반 price adapter.
- `tests/test_r3_price_coverage.py`, `tests/test_pit_membership.py`: OOS 차단, coverage 및 membership leakage에 대한 일반 안전 테스트.
- `research/R4_PLAN.md`: 다음 연구의 사전등록 draft; performance는 미실행.

## GENERALIZE

- `data/r3_validator.py`: PIT membership, OHLC, constituent-date coverage와 hash-independent gate 로직은 R4/향후 dataset audit에도 재사용 가능. 이름 변경은 별도 작은 refactor로 남긴다.
- `data/sources/pit_membership.py`: 현재 R3 운영 경로는 닫혔지만 historical snapshot 재현과 향후 institutional comparison에 사용할 수 있어 dependency가 격리된 상태로 보존한다.

## ARCHIVE

- `data/mapping/ticker_aliases.csv`: 실제 clean retry에 사용된 최소 mapping/provenance 기록. 새로운 연구의 active mapping으로 자동 재사용하지 않는다.
- Local `data/snapshots/r3/r3_free_sp500_v1_audit2` and `r3_free_sp500_clean_retry_v1`: Git ignored historical artifacts. Reports와 manifest가 보존됐으며 향후 삭제 가능하지만 이번에는 파괴적 정리를 하지 않는다.

## REMOVE

- `data/r3_snapshot.py`: checkpoint가 없던 obsolete whole-run builder.
- `data/r3_clean_retry.py`: 마지막 clean attempt 전용 실행기; stop rule 이후 재실행 방지를 위해 제거.
- `research/r3_calibration.py`: clean retry 전용 diagnostic script.
- `research/r3_data_audit.py`: 제거되는 old snapshot loader에 결합된 wrapper.
- `research/r3_replication.py`: R3-001-only authorization/execution wrapper; R3-001이 permanently not authorized이므로 제거.
- 대응하는 clean-retry/snapshot/replication 전용 tests: 제거되는 실행 코드와 함께 제거. 일반 validator/source tests는 유지.
- `data/mapping/unresolved_tickers.csv`: 빈 placeholder. 실제 unresolved 결과는 immutable local snapshot과 report에 보존됨.

삭제는 Git history rewrite나 reset이 아니며 문서화된 uncommitted R3 전용 파일만 대상으로 한다.
