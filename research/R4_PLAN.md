# R4 — Independent Fixed-ETF Universe Replication Plan

## Status

`R4-000 COMPLETE — UNIVERSE FROZEN; R4-001 PERFORMANCE NOT RUN`

## Research Question

Frozen R1-002 momentum/risk-off rule이 개별주식 PIT universe가 아닌, 결과 조회 전에 경제적 범주와 선택 규칙이 고정된 독립 ETF/asset universe에서도 견고성을 보이는가?

R4는 R3의 대체 성공이 아니다. R3는 S&P 500 stock-level PIT replication 데이터 품질 실패로 종료됐으며, R4는 asset-level rotation robustness라는 다른 질문이다.

## Category-first Universe Protocol

성과를 보기 전에 다음 economic exposures를 한 개씩 대표하도록 한다.

1. U.S. broad equity
2. Developed ex-U.S. equity
3. Emerging-market equity
4. U.S. intermediate Treasury
5. U.S. long Treasury
6. U.S. investment-grade corporate bond
7. U.S. listed real estate
8. Gold
9. Broad commodities

### Category boundaries fixed before price inspection

- `U.S. broad equity`: market-cap weighted U.S. total-market or broad large-cap
  index exposure. Style, dividend, factor, sector and thematic funds are excluded.
- `Developed ex-U.S. equity`: diversified developed-market equities excluding the
  United States. Global funds containing the U.S. and single-country funds are excluded.
- `Emerging-market equity`: diversified multi-country emerging-market equities.
- `U.S. intermediate Treasury`: diversified nominal U.S. Treasury exposure whose
  stated index maturity segment is approximately 3–10 years.
- `U.S. long Treasury`: diversified nominal U.S. Treasury exposure whose stated
  index maturity segment begins at approximately 10 years. STRIPS, zero-coupon and
  leveraged-duration products are excluded as specialized exposures.
- `U.S. investment-grade corporate bond`: broad U.S. investment-grade corporate
  credit exposure. Short-, intermediate- and long-only maturity segments are excluded.
- `U.S. listed real estate`: diversified U.S. REIT or listed-real-estate exposure.
- `Gold`: physically backed gold bullion exposure; miners and futures leverage are excluded.
- `Broad commodities`: diversified, multi-commodity futures exposure. Single-commodity
  and sector commodity funds are excluded.

The closed candidate roster and issuer evidence are stored in
`research/R4_CANDIDATES.csv`. It is frozen before any 2013 price/liquidity result is
inspected. Candidate discovery is limited to the issuer product families recorded in
that file; R4-000 does not claim a complete census of every ETF that existed in 2013.

## Eligibility and Representative Selection

- U.S.-listed, unleveraged, non-inverse ETF만 허용한다.
- 단일 산업·테마·국가 ETF는 제외하고 해당 category의 broad exposure만 허용한다.
- ETF inception date는 2010-01-01 이전이어야 한다.
- 최소한 2013-01-01부터 2014-06-30까지 adjusted daily OHLCV가 연속적으로 검증 가능해야 한다.
- 2013 calendar year median daily dollar volume이 USD 5 million 이상이어야 한다.
- 동일 category의 eligible ETF가 여러 개면 2013 median daily dollar volume이 가장 큰 ETF를 선택한다.
- dollar volume이 동일하면 inception date가 더 이른 ETF를 선택하고, 그래도 같으면 ticker 사전순을 사용한다.
- 동일 underlying exposure를 추종하는 중복 ETF는 category별 하나만 남긴다.
- Leveraged ETF와 inverse ETF는 허용하지 않는다.
- Universe freeze date는 2014-06-30이다. 2014-07 이후 정보나 성과로 ETF를 교체하지 않는다.
- 실제 ticker 선정 전 source/version, eligibility table과 제외 이유를 별도 snapshot에 고정한다.

## Frozen Strategy

- Relative momentum lookbacks: 21/63/126 trading days
- Score weights: 1/1/1
- Selection: Top 1
- Winner 126-day absolute momentum `<= 0`: cash
- Rebalance: every 5 trading days
- Signal: close
- Execution: next trading-day open
- Primary slippage: 10bps
- Cost robustness: 0/5/10/20bps
- No Top N/lookback/weight/rebalance search

## Evaluation Protocol

- Development period: 2015-01-01 through 2022-12-31
- Warm-up data: from at least 2014-07-01
- Primary benchmark: SPY buy-and-hold
- Secondary benchmark: frozen ETF universe equal-weight buy-and-hold
- Metrics: cumulative return, CAGR, annual volatility, MDD, Sharpe, Sortino, Calmar, turnover, trades, benchmark/excess return, temporal stability and asset-level P&L concentration
- Transaction-cost scenarios: 0/5/10/20bps; 10bps primary
- Missing data and next-open availability must pass a separate snapshot audit before performance
- Final OOS 2023–2025 remains sealed

## Authorization Gate

R4-000 is authorized only for eligibility verification, 2013 liquidity measurement,
2013-01-01 through 2014-06-30 adjusted-OHLCV quality audit, deterministic representative
selection, and immutable snapshot creation. Strategy signals, portfolio returns,
benchmarks and any R4-001 performance output are prohibited until a separate decision.

## R4-000 Decision Rule

1. Apply non-price eligibility and inception cutoff to the frozen roster.
2. Validate adjusted OHLCV and measure 2013 median `raw close * volume`.
3. Require at least 95% of the common SPY trading dates in both calendar 2013 and
   2014-01-01 through 2014-06-30; missing first/last-period data is not forward-filled.
4. Require zero duplicate dates, zero invalid OHLC rows, non-negative volume, and no
   rows on or after 2023-01-01.
5. Require 2013 median daily dollar volume of at least USD 5,000,000.
6. Within each category select the maximum median dollar volume. Exact ties use earlier
   inception date, then ticker alphabetically.
7. If any category has no passing candidate, R4-000 is `BLOCKED`; thresholds, categories
   and candidates are not changed after observing results.

## R4-000 Frozen Universe

The pre-registered audit passed for all nine categories. The immutable selection is:

`SPY, EFA, EEM, IEF, TLT, LQD, IYR, GLD, DBC`

Detailed eligibility, liquidity, coverage and failure evidence is recorded in
`research/results/R4-000-fixed-etf-universe-audit.md`. R4-001 remains unexecuted and
requires a separate authorization decision.
