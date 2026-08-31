# R4B — Broad ETF Cross-sectional Replication Plan

## Status

`R4B CLOSED — BLOCKED BY FREE-DATA COVERAGE; PERFORMANCE NOT AUTHORIZED`

## Research Question

Frozen R1-002가 9개 macro asset 대표가 아니라 결과와 무관하게 구성된 더 넓은
ETF exposure universe에서도 특정 ETF·category·regime에 의존하지 않고 재현되는가?

R4B는 R4A를 대체하거나 R4A 결과에 따라 universe를 재설계하지 않는다.

## Frozen Strategy

R4A와 동일하게 21/63/126, weights 1/1/1, Top 1, winner 126-day momentum
`<= 0` cash, 5-day rebalance, close signal/next-open execution, 10bps primary 및
0/5/10/20bps robustness를 사용한다. Parameter search는 없다.

## R4B-000 Universe and Data Gate

- Universe as-of/freeze date: 2014-06-30.
- U.S.-listed ETF, inception before 2010-01-01, unleveraged, non-inverse.
- Single-stock products 제외. Equity style/size/sector, international regions,
  government maturity, credit, inflation-linked bonds, real estate, diversified
  commodities, precious metals 및 currencies의 taxonomy를 가격 결과 전에 고정한다.
- 동일 underlying index 또는 실질적으로 동일한 exposure는 하나의 family로 묶고,
  2013 median raw-close dollar volume 최대 ETF 하나를 선택한다.
- Minimum 2013 median dollar volume: USD 5M. Coverage 및 OHLC gate는 R4A-000과 동일.
- Historical ETF master에는 2014-06-30 당시 존재했으나 이후 청산·합병된 ETF가
  포함돼야 한다. 현재 생존 ETF 목록만으로 구성하지 않는다.
- Ticker change, merger, liquidation date, terminal-value 처리와 adjusted next-open
  availability를 검증해야 한다. 누락 ETF를 silent drop하지 않는다.
- Exposure family 수, category별 family 수, source/version, exclusions와 mapping을
  성과 조회 전에 immutable snapshot으로 고정한다.

Historical master, liquidated ETF 또는 terminal treatment가 불충분하면 R4B-000은
`BLOCKED` 또는 `CONDITIONAL`이며 R4B-001은 실행하지 않는다. R4A 결과를 이유로
gate나 taxonomy를 변경하지 않는다.

## Evaluation Boundary

- Development: 2015–2022, warm-up from 2014-07-01.
- Benchmarks: SPY 및 frozen broad-universe equal-weight buy-and-hold.
- 필수 diagnostics: ETF와 category별 P&L concentration, effective independent
  exposure count, selection frequency, holding period, temporal stability, cost sensitivity.
- Final OOS 2023–2025: SEALED.
- R4B-001 performance: separate authorization required after R4B-000 adjudication.

## R4B-000 Feasibility Outcome

- CRSP Survivor-Bias-Free U.S. Mutual Fund Database는 ETF/ETN flag, active/inactive
  funds, historical header, liquidation/merger status와 acquiring-fund 정보를 제공하므로
  구조적으로 가장 가까운 source다. 그러나 subscription/license가 필요하고 현재 project는
  sample 또는 row-level access를 보유하지 않는다.
- Nasdaq 공개 symbol directory는 current-day directory다. Historical Daily List는
  listing/delisting/name/symbol events를 제공하는 보조 source지만, 이것만으로 완전한
  historical ETF master, exposure taxonomy, adjusted OHLC와 liquidation proceeds를
  재구성할 수 없다.
- Yahoo/current issuer roster는 inactive ETF completeness를 보장하지 못하므로 primary
  universe source로 허용하지 않는다.

판정은 `CONDITIONAL — DATA EXISTS, ACCESS NOT VERIFIED`다. CRSP 또는 동등한 licensed
dataset의 실제 접근·sample validation 없이는 R4B-001을 실행하지 않는다. 현재 ETF만으로
축소하거나 missing funds를 제거해 결과를 만들지 않는다.

## Free-data-only Final Adjudication

사용자는 R4B를 무료 데이터로만 진행하기로 결정했다. 제한된 공식-source audit 결과:

- SEC EDGAR submissions와 filing archives는 무료이며 former names와 filing history를
  포함하지만, 2014-06-30 ETF master, exchange ticker effective history, exposure family,
  delisting/merger terminal proceeds와 adjusted OHLC를 하나의 검증 가능한 schema로
  제공하지 않는다.
- SEC structured N-CEN/N-PORT data는 R4B의 2014 freeze date를 재구성하기에 시기가
  늦다. Raw pre-2014 filings를 대규모로 parsing해도 exchange tradability와 terminal
  price gate가 별도로 남는다.
- Nasdaq historical Daily List는 1999년 이후 events를 제공하지만 monthly subscription
  product이며 무료 제약을 충족하지 않는다.
- Current symbol directory, current ETF screen, Yahoo와 issuer closure notices를 조합하면
  completeness를 측정할 denominator가 없고 ticker/exposure mapping을 수작업 추정하게 된다.

따라서 `R4B CLOSED — BLOCKED BY FREE-DATA COVERAGE`. R4B-001은 무료-data protocol에서
permanently `NOT AUTHORIZED`다. 무료 threshold를 완화하거나 survivor-only universe로
대체하지 않는다. Licensed historical master를 도입하는 새로운 decision이 있을 때만
R4B를 재개할 수 있다.
