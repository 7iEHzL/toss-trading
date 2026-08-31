# Alpha Lab Data Feasibility

## Tier 1 — reliable enough within a stated scope

- Daily adjusted OHLCV for currently active, liquid securities/ETFs when cached in immutable snapshots
  and validated against splits, missing rows and date bounds.
- FRED/ALFRED macro series with explicit vintage/release handling.
- Prospectively frozen universe membership and identifier history collected after Alpha Lab freeze.

Tier 1 does not imply institutional-grade tick data or survivorship-free prehistory.

## Tier 2 — usable with material limitations

- Yahoo historical OHLCV: useful for discovery, but delisted coverage and adjusted-price provenance are
  incomplete.
- Current broad US listings applied historically: survivorship/selection biased.
- SEC filings and free fundamentals: possible, but filing availability dates, restatements, identifiers and
  standardized history require a dedicated PIT pipeline.
- Current sector/industry classifications: historical classification drift is not controlled.
- Free earnings/corporate-action metadata: coverage and exact announcement timing require audit.

Results must carry explicit bias flags and cannot be promoted as clean historical validation.

## Tier 3 — unsuitable without licensed/institutional data

- Survivorship-free historical US equity/ETF master with complete delistings and terminal returns.
- Standardized point-in-time fundamentals and analyst-estimate vintages at broad scale.
- Reliable historical index membership plus identifier/corporate-action chains.
- Intraday quote/trade data suitable for microstructure execution claims.

R3 and R4B already demonstrated that free Yahoo/current-directory stitching cannot close these gaps.

## Layer contract

Future code should separate immutable `raw` snapshots, schema/timestamp-checked `validated` data,
versioned `features`, signed `signals`, horizon-specific `forward_returns`, immutable `results`, and
human-readable `metadata`. Each derived artifact records parent hashes, code version, universe snapshot,
calendar, timezone and latest permissible source timestamp.
