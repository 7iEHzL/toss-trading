# Initial Alpha Batch — Pipeline Calibration Only

All entries are `PROPOSED`. Parameters, final universe and numeric decision gates must be frozen in
individual Alpha Cards before testing. No performance is authorized.

| ID | Family | Hypothesis / formula concept | Data | Expected sign | Literature anchor | Turnover | Main bias risk | Calibration value |
|---|---|---|---|---|---|---|---|---|
| A001 | PRICE | Cross-sectional medium-term momentum: rank lagged cumulative return, excluding the most recent month | Adjusted close | Positive | Jegadeesh–Titman momentum | Medium | survivor/microcap and horizon freedom | basic ranks/forward returns |
| A002 | PRICE | Short-horizon reversal: negative rank of recent return | Adjusted close | Positive for reversal score | Jegadeesh short-run reversal literature | High | spread/cost dominance | timing and cost stress |
| A003 | PRICE | Nearness to prior 52-week high | Adjusted close/high | Positive | George–Hwang | Medium | split adjustment/lookback | rolling feature validation |
| A004 | VOLUME_LIQUIDITY | Price direction conditioned on abnormal volume relative to its own history | OHLCV | Same-direction continuation | volume-return literature | High | volume definition and interaction freedom | volume schema/coverage |
| A005 | VOLUME_LIQUIDITY | Deterioration in Amihud-style illiquidity, ranked cross-sectionally | return, dollar volume | Higher illiquidity premium | Amihud | Medium | microcap/outlier domination | winsorization and liquidity gates |
| A006 | VOLATILITY | Low idiosyncratic/realized volatility rank | Daily returns; benchmark if idiosyncratic | Lower volatility predicts higher risk-adjusted future return | low-volatility anomaly literature | Low–medium | beta/size confounding | neutralization diagnostics |
| A007 | FUNDAMENTAL | Earnings yield/value rank using only filed-and-available accounting data | PIT market cap/earnings | Positive | value literature | Low | restatements and filing lag | PIT fundamental gate |
| A008 | FUNDAMENTAL | Gross profitability scaled by assets | PIT statements | Positive | Novy-Marx profitability | Low | standardized fundamentals unavailable | DATA_BLOCKED path test |
| A009 | EVENT | Post-earnings-announcement drift from timestamped standardized surprise | earnings timestamps/expectations, prices | Same sign as surprise | PEAD literature | Medium | announcement/estimate PIT leakage | event clock validation |
| A010 | INTERACTION | Medium-term momentum attenuated by high realized volatility | adjusted prices | Positive, stronger for lower-vol momentum | momentum/volatility literature | Medium | data-driven interaction choice | lineage and redundancy controls |

The batch spans simple known anomalies so failures diagnose the pipeline rather than inspire immediate
retuning. A007–A009 may correctly become `DATA_BLOCKED` under free-data constraints.
