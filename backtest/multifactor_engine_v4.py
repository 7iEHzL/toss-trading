import pandas as pd

from backtest.accounting import build_backtest_result, execute_target_rebalance
from backtest.portfolio import Portfolio
from backtest.research import static_fundamentals_disclosure


def rank_series(series, higher_is_better=True):
    if higher_is_better:
        return series.rank(pct=True)
    return series.rank(pct=True, ascending=False)


def run_multifactor_rotation_backtest_v4(
    data_dict,
    fundamental_data,
    initial_cash=10000000,
    momentum_lookback=63,
    absolute_momentum_lookback=126,
    volume_lookback=20,
    ma_window=120,
    rebalance_interval=5,
    top_n=2,
    atr_window=20,
    atr_multiplier=3.0,
    weight_momentum=0.40,
    weight_quality=0.25,
    weight_value=0.25,
    weight_volume=0.10,
    cost_model=None,
    benchmark=None,
):
    if not data_dict:
        raise ValueError("종목 데이터가 비어 있습니다.")

    close_df = pd.DataFrame()
    open_df = pd.DataFrame()
    high_df = pd.DataFrame()
    low_df = pd.DataFrame()
    volume_df = pd.DataFrame()

    for ticker, df in data_dict.items():
        required_columns = {"date", "open", "high", "low", "close", "volume"}
        missing_columns = required_columns.difference(df.columns)
        if missing_columns:
            missing_text = ", ".join(sorted(missing_columns))
            raise ValueError(f"{ticker} 필수 컬럼이 없습니다: {missing_text}")

        temp = df.copy()
        temp["date"] = pd.to_datetime(temp["date"])
        temp = temp.sort_values("date").set_index("date")

        close_df[ticker] = temp["close"]
        open_df[ticker] = temp["open"]
        high_df[ticker] = temp["high"]
        low_df[ticker] = temp["low"]
        volume_df[ticker] = temp["volume"]

    valid_rows = (
        close_df.notna().all(axis=1)
        & open_df.notna().all(axis=1)
        & high_df.notna().all(axis=1)
        & low_df.notna().all(axis=1)
        & volume_df.notna().all(axis=1)
    )
    close_df = close_df.loc[valid_rows]
    open_df = open_df.loc[valid_rows]
    high_df = high_df.loc[close_df.index]
    low_df = low_df.loc[close_df.index]
    volume_df = volume_df.loc[close_df.index]

    tickers = list(close_df.columns)

    ma_df = close_df.rolling(ma_window).mean()
    ma5_df = close_df.rolling(5).mean()
    ma20_df = close_df.rolling(20).mean()

    delta = close_df.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    rsi_df = 100 - (100 / (1 + rs))

    # ATR 계산
    prev_close = close_df.shift(1)
    tr1 = high_df - low_df
    tr2 = (high_df - prev_close).abs()
    tr3 = (low_df - prev_close).abs()
    tr = pd.concat([tr1.stack(), tr2.stack(), tr3.stack()], axis=1).max(axis=1).unstack()
    atr_df = tr.rolling(atr_window).mean()

    portfolio = Portfolio(initial_cash, cost_model)
    highest_price = {}

    equity_curve = []
    rebalance_logs = []
    pending_stop_signals = {}
    pending_rebalance = None

    start_index = max(
        momentum_lookback,
        absolute_momentum_lookback,
        volume_lookback * 2,
        ma_window,
        atr_window,
        20,
        14
    )

    if len(close_df) <= start_index:
        raise ValueError(
            f"데이터 부족: 필요 {start_index + 1}, 현재 {len(close_df)}"
        )

    for i in range(start_index, len(close_df)):
        today = close_df.index[i]
        close_prices = close_df.iloc[i]
        open_prices = open_df.iloc[i]

        # 전 거래일 종가에 발생한 ATR stop을 당일 시가에 실행
        for ticker, signal_date in list(pending_stop_signals.items()):
            if portfolio.quantity(ticker):
                portfolio.liquidate(
                    ticker, open_prices[ticker], index=len(equity_curve),
                    date=today, signal_date=signal_date, reason="ATR_STOP",
                )
                highest_price.pop(ticker, None)
        pending_stop_signals = {}

        # 전 거래일 종가에 확정한 리밸런싱을 당일 시가에 실행
        if pending_rebalance is not None:
            winners = pending_rebalance["winners"]
            scores = pending_rebalance["scores"]
            signal_date = pending_rebalance["signal_date"]

            old_symbols = set(portfolio.holdings)
            execute_target_rebalance(
                portfolio, winners, open_prices, len(equity_curve),
                today, signal_date, scores, reason="REBALANCE",
            )
            for ticker in old_symbols.difference(portfolio.holdings):
                highest_price.pop(ticker, None)
            for ticker in portfolio.holdings:
                highest_price[ticker] = max(
                    highest_price.get(ticker, open_prices[ticker]), open_prices[ticker]
                )
            pending_rebalance = None

        # =========================
        # 1. ATR Trailing Stop 체크
        # =========================
        for ticker, qty in list(portfolio.holdings.items()):
            current_price = close_prices[ticker]
            atr = atr_df.iloc[i][ticker]

            if pd.isna(atr):
                continue

            highest_price[ticker] = max(
                highest_price.get(ticker, current_price),
                current_price
            )

            stop_price = highest_price[ticker] - atr_multiplier * atr

            if current_price < stop_price:
                if i + 1 < len(close_df):
                    pending_stop_signals[ticker] = today

        is_rebalance_day = (i - start_index) % rebalance_interval == 0

        # =========================
        # 2. 리밸런싱
        # =========================
        if is_rebalance_day:
            momentum = close_df.iloc[i] / close_df.iloc[i - momentum_lookback] - 1
            absolute_momentum = close_df.iloc[i] / close_df.iloc[i - absolute_momentum_lookback] - 1

            recent_volume = volume_df.iloc[i - volume_lookback:i].mean()
            past_volume = volume_df.iloc[i - volume_lookback * 2:i - volume_lookback].mean()
            volume_raw = recent_volume / past_volume - 1

            roe = pd.Series({
                ticker: fundamental_data[ticker]["roe"]
                for ticker in tickers
            })

            pbr = pd.Series({
                ticker: fundamental_data[ticker]["pbr"]
                for ticker in tickers
            })

            momentum_rank = rank_series(momentum, True)
            volume_rank = rank_series(volume_raw, True)
            quality_rank = rank_series(roe, True)
            value_rank = rank_series(pbr, False)

            total_score = (
                weight_momentum * momentum_rank
                + weight_quality * quality_rank
                + weight_value * value_rank
                + weight_volume * volume_rank
            )

            candidates = []
            rejected = {}

            for ticker in tickers:
                reasons = []

                if absolute_momentum[ticker] <= 0:
                    reasons.append("absolute_momentum<=0")

                if close_prices[ticker] <= ma_df.iloc[i][ticker]:
                    reasons.append("close<=MA")

                if ma5_df.iloc[i][ticker] <= ma20_df.iloc[i][ticker]:
                    reasons.append("MA5<=MA20")

                if rsi_df.iloc[i][ticker] <= 55:
                    reasons.append("RSI<=55")

                if len(reasons) == 0:
                    candidates.append(ticker)
                else:
                    rejected[ticker] = reasons

            if len(candidates) > 0:
                winners = (
                    total_score.loc[candidates]
                    .sort_values(ascending=False)
                    .head(top_n)
                    .index
                    .tolist()
                )
            else:
                winners = []

            rebalance_logs.append({
                "index": len(equity_curve),
                "date": today,
                "execution_date": (
                    close_df.index[i + 1] if i + 1 < len(close_df) else None
                ),
                "winners": winners,
                "candidates": candidates,
                "rejected": rejected,
                "scores": total_score.to_dict()
            })

            if i + 1 < len(close_df):
                pending_rebalance = {
                    "winners": winners,
                    "scores": total_score.to_dict(),
                    "signal_date": today,
                }

        current_equity = portfolio.equity(close_prices)

        equity_curve.append(current_equity)

    return build_backtest_result(
        portfolio, equity_curve, close_df.index[start_index:], initial_cash,
        close_df.iloc[-1], benchmark,
        research_disclosure=static_fundamentals_disclosure(),
        open_df=open_df, close_df=close_df,
        rebalance_logs=rebalance_logs,
    )
