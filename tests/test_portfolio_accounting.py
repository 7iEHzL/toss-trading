import unittest

from backtest.costs import ExecutionCostModel
from backtest.portfolio import Portfolio


class PortfolioAccountingTests(unittest.TestCase):
    def test_average_cost_and_partial_sale_realized_pnl_include_costs(self):
        portfolio = Portfolio(1000, ExecutionCostModel(0.01, 100))
        portfolio.buy("AAA", 4, 100, date="d1")
        portfolio.buy("AAA", 2, 120, date="d2")

        self.assertAlmostEqual(portfolio.average_cost("AAA"), 108.81066666666668)
        trade = portfolio.sell("AAA", 3, 130, date="d3")
        self.assertAlmostEqual(trade["price"], 128.7)
        self.assertAlmostEqual(trade["realized_pnl"], 55.807)
        self.assertEqual(portfolio.quantity("AAA"), 3)
        self.assertAlmostEqual(portfolio.realized_pnl, 55.807)
        self.assertAlmostEqual(portfolio.unrealized_pnl({"AAA": 125}), 48.568)
        self.assertAlmostEqual(trade["cost_basis_sold"], 326.432)
        self.assertAlmostEqual(
            portfolio.initial_cash + portfolio.realized_pnl
            + portfolio.unrealized_pnl({"AAA": 125}),
            portfolio.equity({"AAA": 125}),
        )

    def test_target_weight_rebalance_sells_overweight_position(self):
        portfolio = Portfolio(1000)
        portfolio.buy("AAA", 8, 100)
        portfolio.rebalance({"AAA": 0.5, "BBB": 0.5}, {"AAA": 100, "BBB": 100})

        self.assertEqual(portfolio.holdings, {"AAA": 5, "BBB": 5})
        self.assertEqual([trade["action"] for trade in portfolio.trades], ["BUY", "SELL", "BUY"])
        self.assertAlmostEqual(portfolio.cash, 0.0)

    def test_rebalance_to_cash_closes_position_and_counts_realized_win(self):
        portfolio = Portfolio(1000)
        portfolio.buy("AAA", 10, 100)
        portfolio.rebalance({}, {"AAA": 110})
        summary = portfolio.summary({})

        self.assertEqual(summary["holdings"], {})
        self.assertEqual(summary["wins"], 1)
        self.assertEqual(summary["win_rate"], 100.0)
        self.assertEqual(summary["realized_pnl"], 100.0)


if __name__ == "__main__":
    unittest.main()
