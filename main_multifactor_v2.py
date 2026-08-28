from api.auth import get_access_token
from api.candle import get_daily_candles

from data.fundamental_data import FUNDAMENTAL_DATA
from backtest.multifactor_engine_v2 import run_multifactor_rotation_backtest_v2
from backtest.visualizer import plot_equity_curve


TICKERS = [
    "AMD", "TSLA", "AMZN", "AAPL", "SPXL",
    "QQQ", "SOXX", "SMH", "NVDA", "MSFT",
    "META", "GOOGL", "AVGO"
]

INITIAL_CASH = 10000000
CANDLE_COUNT = 200

token = get_access_token()

if not token:
    print("토큰 발급 실패")
    exit()

print("토큰 발급 성공!")

data_dict = {}

import time

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

    data_dict[ticker] = df
    print(f"{ticker} 데이터 조회 완료: {len(df)}개")

    time.sleep(1.5)


result = run_multifactor_rotation_backtest_v2(
    data_dict=data_dict,
    fundamental_data=FUNDAMENTAL_DATA,
    initial_cash=INITIAL_CASH,
    momentum_lookback=63,
    absolute_momentum_lookback=126,
    volume_lookback=20,
    ma_window=120, #200,
    rebalance_interval=5,
    top_n=2,
    weight_momentum=0.40,
    weight_quality=0.25,
    weight_value=0.25,
    weight_volume=0.10
)

print("\n===== Multifactor v2 백테스트 결과 =====")
print(f"초기 자금: {result['initial_cash']:,}원")
print(f"최종 자산: {int(result['final_value']):,}원")
print(f"총 수익률: {result['return_pct']:.2f}%")
print(f"최대 낙폭(MDD): {result['mdd']:.2f}%")
print(f"승리 거래: {result['wins']}")
print(f"패배 거래: {result['losses']}")
print(f"승률: {result['win_rate']:.2f}%")

print("\n===== 거래 내역 =====")
for trade in result["trades"]:
    print(
        trade["date"].date(),
        trade["action"],
        trade["symbol"],
        f"가격: {trade['price']}",
        f"수량: {trade['qty']}"
    )

print("\n===== 리밸런싱 기록 =====")
for log in result["rebalance_logs"]:
    print(
        log["date"].date(),
        "Winners:",
        log["winners"],
        "Candidates:",
        log["candidates"]
    )

plot_equity_curve(
    result,
    symbol="Multifactor v2 Top2 Rotation"
)