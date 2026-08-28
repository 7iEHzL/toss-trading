from api.auth import get_access_token
from api.candle import get_daily_candles

from backtest.rotation_engine import run_rotation_backtest
from backtest.visualizer import plot_equity_curve


# =========================
# 전략 설정
# =========================

TICKERS = ["AMD", "TSLA", "AMZN", "AAPL", "SPXL"]

INITIAL_CASH = 10000000

CANDLE_COUNT = 200

REBALANCE_INTERVAL = 5  # 5거래일마다 리밸런싱, 대략 주 1회

LOOKBACK_1M = 21
LOOKBACK_3M = 63
LOOKBACK_6M = 126


# =========================
# 데이터 로드
# =========================


def main():
    token = get_access_token()

    if not token:
        print("토큰 발급 실패")
        exit()

    print("토큰 발급 성공!")

    data_dict = {}

    for ticker in TICKERS:
        print(f"\n{ticker} 캔들 데이터 조회 중...")

        df = get_daily_candles(
            access_token=token,
            symbol=ticker,
            count=CANDLE_COUNT
        )

        if df is None:
            print(f"{ticker} 데이터 조회 실패")
            exit()

        if len(df) < LOOKBACK_6M:
            print(f"{ticker} 데이터 부족: {len(df)}개")
            exit()

        data_dict[ticker] = df

        print(f"{ticker} 데이터 조회 완료: {len(df)}개")


    # =========================
    # 로테이션 백테스트 실행
    # =========================

    result = run_rotation_backtest(
        data_dict=data_dict,
        initial_cash=INITIAL_CASH,
        lookback_1m=LOOKBACK_1M,
        lookback_3m=LOOKBACK_3M,
        lookback_6m=LOOKBACK_6M,
        weight_1m=1.0,
        weight_3m=1.0,
        weight_6m=1.0,
        rebalance_interval=REBALANCE_INTERVAL
    )


    # =========================
    # 결과 출력
    # =========================

    print("\n===== Cross-Sectional Momentum Rotation 백테스트 결과 =====")

    print(f"초기 자금: {result['initial_cash']:,}원")
    print(f"최종 자산: {int(result['final_value']):,}원")
    print(f"총 수익률: {result['return_pct']:.2f}%")
    print(f"최대 낙폭(MDD): {result['mdd']:.2f}%")
    print(f"승리 거래: {result['wins']}")
    print(f"패배 거래: {result['losses']}")
    print(f"승률: {result['win_rate']:.2f}%")

    print("\n===== 거래 내역 =====")

    trade_count = 0

    for trade in result["trades"]:
        trade_count += 1

        print(
            trade["date"].date(),
            trade["action"],
            trade["symbol"],
            f"가격: {trade['price']}",
            f"수량: {trade['qty']}"
        )

    print(f"\n총 거래 기록 수: {trade_count}")


    # =========================
    # 그래프 출력
    # =========================

    plot_equity_curve(
        result,
        symbol="AMD_TSLA_AMZN_AAPL_SPXL Rotation"
    )

    print("\n===== 리밸런싱 기록 =====")

    for log in result["rebalance_logs"]:
        print(
            log["date"].date(),
            "Winner:",
            log["winner"],
            "Score:",
            round(log["winner_score"], 4),
            "Changed:",
            log["changed"]
        )


if __name__ == "__main__":
    main()
