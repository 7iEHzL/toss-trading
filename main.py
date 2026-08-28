from api.auth import get_access_token
from api.candle import get_daily_candles

from backtest.multi_strategy import compare_strategies


token = get_access_token()

if token:
    print("토큰 발급 성공!")

    df = get_daily_candles(
        access_token=token,
        symbol="005930",
        count=200
    )
    if df is None:
        print("캔들 데이터 조회 실패")
        exit()

    results = compare_strategies(
        df,
        initial_cash=10000000
    )

    print("\n===== 전략별 백테스트 비교 =====")

    for r in results:
        print("\n전략:", r["strategy"])
        print(f"최종 자산: {int(r['final_value']):,}원")
        print(f"수익률: {r['return_pct']:.2f}%")
        print(f"MDD: {r['mdd']:.2f}%")
        print(f"승률: {r['win_rate']:.2f}%")
        print(f"거래 횟수: {r['trades']}")