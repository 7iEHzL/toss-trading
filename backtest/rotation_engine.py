import pandas as pd


def run_rotation_backtest(
    data_dict,
    initial_cash=10000000,
    lookback_1m=21,
    lookback_3m=63,
    lookback_6m=126,
    weight_1m=1.0,
    weight_3m=1.0,
    weight_6m=1.0,
    rebalance_interval=5
):
    """
    횡단면 모멘텀 로테이션 백테스트 엔진

    data_dict 예시:
    {
        "AMD": df_amd,
        "TSLA": df_tsla,
        "AMZN": df_amzn,
        "AAPL": df_aapl,
        "SPXL": df_spxl
    }

    각 df에는 반드시 date, close 컬럼이 있어야 함.
    """

    # =========================
    # 1. 종가 데이터 정리
    # =========================

    close_df = pd.DataFrame()

    for ticker, df in data_dict.items():
        temp = df.copy()
        temp["date"] = pd.to_datetime(temp["date"])
        temp = temp.sort_values("date")
        temp = temp.set_index("date")

        close_df[ticker] = temp["close"]

    close_df = close_df.dropna()

    # =========================
    # 2. 모멘텀 점수 계산
    # =========================

    score_df = (
        weight_1m * close_df.pct_change(lookback_1m)
        + weight_3m * close_df.pct_change(lookback_3m)
        + weight_6m * close_df.pct_change(lookback_6m)
    )

    # =========================
    # 3. 백테스트 상태 변수
    # =========================

    cash = initial_cash
    holding = None
    quantity = 0

    trades = []
    rebalance_logs = []
    equity_curve = []
    holding_history = []

    start_index = max(
        lookback_1m,
        lookback_3m,
        lookback_6m
    )

    # =========================
    # 4. 리밸런싱 백테스트
    # =========================

    for i in range(start_index, len(close_df)):

        today = close_df.index[i]

        prices = close_df.iloc[i]
        scores = score_df.iloc[i]

        # 현재 자산 평가
        current_equity = cash

        if holding is not None:
            current_equity += quantity * prices[holding]

        # 리밸런싱 날짜 여부
        is_rebalance_day = (
            (i - start_index) % rebalance_interval == 0
        )

        if is_rebalance_day:

            # 모멘텀 점수가 가장 높은 종목 선택
            winner = scores.idxmax()
            winner_score = scores[winner]
            rebalance_logs.append({
                "index": len(equity_curve),
                "date": today,
                "winner": winner,
                "winner_score": winner_score,
                "holding": holding,
                "changed": holding != winner,
                "scores": scores.to_dict()
            })

            # 점수가 NaN이면 패스
            if pd.isna(winner_score):
                equity_curve.append(current_equity)
                holding_history.append(holding)
                continue

            # 기존 보유 종목과 다르면 교체
            if holding != winner:

                # 기존 종목 매도
                if holding is not None:
                    sell_price = prices[holding]
                    cash += quantity * sell_price

                    trades.append({
                        "index": len(equity_curve),
                        "date": today,
                        "action": "SELL",
                        "symbol": holding,
                        "price": sell_price,
                        "qty": quantity,
                        "cash": cash
                    })

                    quantity = 0
                    holding = None

                # 신규 종목 매수
                buy_price = prices[winner]
                quantity = cash // buy_price

                if quantity > 0:
                    cash -= quantity * buy_price
                    holding = winner

                    trades.append({
                        "index": len(equity_curve),
                        "date": today,
                        "action": "BUY",
                        "symbol": winner,
                        "price": buy_price,
                        "qty": quantity,
                        "cash": cash,
                        "score": winner_score
                    })

        # 리밸런싱 후 자산 재평가
        current_equity = cash

        if holding is not None:
            current_equity += quantity * prices[holding]

        equity_curve.append(current_equity)
        holding_history.append(holding)

    # =========================
    # 5. 최종 성과 계산
    # =========================

    final_value = equity_curve[-1]

    return_pct = (
        (final_value - initial_cash)
        / initial_cash
        * 100
    )

    # MDD 계산
    peak = equity_curve[0]
    mdd = 0
    mdd_peak_index = 0
    mdd_trough_index = 0
    temp_peak_index = 0

    for i, equity in enumerate(equity_curve):

        if equity > peak:
            peak = equity
            temp_peak_index = i

        drawdown = (equity - peak) / peak

        if drawdown < mdd:
            mdd = drawdown
            mdd_peak_index = temp_peak_index
            mdd_trough_index = i

    mdd *= 100

    # 승률 계산
    wins = 0
    losses = 0

    for i in range(1, len(trades), 2):
        buy = trades[i - 1]
        sell = trades[i]

        if buy["action"] == "BUY" and sell["action"] == "SELL":
            if sell["price"] > buy["price"]:
                wins += 1
            else:
                losses += 1

    total_closed = wins + losses
    win_rate = wins / total_closed * 100 if total_closed > 0 else 0

    return {
        "initial_cash": initial_cash,
        "final_value": final_value,
        "return_pct": return_pct,
        "mdd": mdd,
        "mdd_peak_index": mdd_peak_index,
        "mdd_trough_index": mdd_trough_index,
        "trades": trades,
        "equity_curve": equity_curve,
        "holding_history": holding_history,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate,
        "score_df": score_df,
        "close_df": close_df,
        "rebalance_logs": rebalance_logs
    }