import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def plot_equity_curve(result, symbol="Backtest"):
    equity_curve = result["equity_curve"]
    trades = result["trades"]

    plt.figure(figsize=(17, 9))

    plt.plot(
        equity_curve,
        color="blue",
        linewidth=2.2,
        label="Equity Curve"
    )

    # MDD 구간 표시
    if "mdd_peak_index" in result and "mdd_trough_index" in result:
        peak_i = result["mdd_peak_index"]
        trough_i = result["mdd_trough_index"]

        plt.axvspan(
            peak_i,
            trough_i,
            alpha=0.15,
            color="red",
            label="MDD Section"
        )

        plt.scatter(
            peak_i,
            equity_curve[peak_i],
            marker="o",
            s=120,
            color="red",
            zorder=6,
            label="MDD Peak"
        )

        plt.scatter(
            trough_i,
            equity_curve[trough_i],
            marker="x",
            s=160,
            color="red",
            zorder=6,
            label="MDD Trough"
        )

    buy_label_used = False
    sell_label_used = False

    for trade in trades:
        x = trade["index"]

        if x < 0 or x >= len(equity_curve):
            continue

        y = equity_curve[x]

        action = trade["action"]
        ticker = trade.get("symbol", "")
        price = trade["price"]
        qty = trade["qty"]

        if action == "BUY":
            plt.scatter(
                x,
                y,
                marker="^",
                s=180,
                color="green",
                edgecolors="black",
                linewidths=0.8,
                zorder=7,
                label="BUY" if not buy_label_used else ""
            )

            plt.annotate(
                f"BUY {ticker}\n{price:,.2f}\nqty {int(qty):,}",
                xy=(x, y),
                xytext=(0, 45),
                textcoords="offset points",
                ha="center",
                fontsize=8,
                color="green",
                bbox=dict(
                    boxstyle="round,pad=0.3",
                    fc="white",
                    ec="green",
                    alpha=0.85
                ),
                arrowprops=dict(
                    arrowstyle="->",
                    color="green",
                    lw=1
                )
            )

            buy_label_used = True

        elif action == "SELL":
            plt.scatter(
                x,
                y,
                marker="v",
                s=180,
                color="red",
                edgecolors="black",
                linewidths=0.8,
                zorder=7,
                label="SELL" if not sell_label_used else ""
            )

            plt.annotate(
                f"SELL {ticker}\n{price:,.2f}\nqty {int(qty):,}",
                xy=(x, y),
                xytext=(0, -60),
                textcoords="offset points",
                ha="center",
                fontsize=8,
                color="red",
                bbox=dict(
                    boxstyle="round,pad=0.3",
                    fc="white",
                    ec="red",
                    alpha=0.85
                ),
                arrowprops=dict(
                    arrowstyle="->",
                    color="red",
                    lw=1
                )
            )

            sell_label_used = True

    plt.title(
        f"{symbol} Backtest Equity Curve",
        fontsize=20,
        fontweight="bold"
    )

    plt.xlabel("Trading Days", fontsize=12)
    plt.ylabel("Asset Value (KRW)", fontsize=12)

    plt.grid(alpha=0.25)

    plt.gca().yaxis.set_major_formatter(
        FuncFormatter(lambda x, p: f"{int(x):,}")
    )

    handles, labels = plt.gca().get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    plt.legend(
        unique.values(),
        unique.keys(),
        loc="upper left"
    )

    plt.tight_layout()
    plt.show()