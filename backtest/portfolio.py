import math

from backtest.costs import ExecutionCostModel


class Portfolio:
    """Long-only portfolio ledger with average-cost accounting."""

    def __init__(self, initial_cash, cost_model=None):
        if not math.isfinite(initial_cash) or initial_cash < 0:
            raise ValueError("initial_cash must be a finite non-negative number")
        self.initial_cash = float(initial_cash)
        self.cash = float(initial_cash)
        self.cost_model = cost_model or ExecutionCostModel()
        self.positions = {}
        self.trades = []
        self.realized_pnl = 0.0
        self.total_commission = 0.0
        self.total_slippage_cost = 0.0

    @property
    def holdings(self):
        return {symbol: position["quantity"] for symbol, position in self.positions.items()}

    def quantity(self, symbol):
        return self.positions.get(symbol, {}).get("quantity", 0)

    def average_cost(self, symbol):
        return self.positions.get(symbol, {}).get("average_cost", 0.0)

    def equity(self, prices):
        return self.cash + sum(
            position["quantity"] * float(prices[symbol])
            for symbol, position in self.positions.items()
        )

    def unrealized_pnl(self, prices):
        return sum(
            position["quantity"]
            * (float(prices[symbol]) - position["average_cost"])
            for symbol, position in self.positions.items()
        )

    def buy(self, symbol, quantity, reference_price, **metadata):
        quantity = int(quantity)
        if quantity <= 0:
            return None
        fill_price = self.cost_model.fill_price("BUY", float(reference_price))
        notional = fill_price * quantity
        commission = self.cost_model.commission(notional)
        total_cost = notional + commission
        if total_cost > self.cash + 1e-9:
            raise ValueError("insufficient cash for buy")

        old_quantity = self.quantity(symbol)
        old_basis = old_quantity * self.average_cost(symbol)
        new_quantity = old_quantity + quantity
        average_cost = (old_basis + total_cost) / new_quantity
        self.cash -= total_cost
        self.positions[symbol] = {
            "quantity": new_quantity,
            "average_cost": average_cost,
        }
        trade = self._record_trade(
            "BUY", symbol, quantity, reference_price, fill_price,
            commission, 0.0, average_cost, **metadata
        )
        trade["net_cash_flow"] = -total_cost
        trade["cost_basis_added"] = total_cost
        return trade

    def sell(self, symbol, quantity, reference_price, **metadata):
        quantity = int(quantity)
        held = self.quantity(symbol)
        if quantity <= 0:
            return None
        if quantity > held:
            raise ValueError("sell quantity exceeds position")

        average_cost = self.average_cost(symbol)
        fill_price = self.cost_model.fill_price("SELL", float(reference_price))
        notional = fill_price * quantity
        commission = self.cost_model.commission(notional)
        realized_pnl = notional - commission - average_cost * quantity
        self.cash += notional - commission
        self.realized_pnl += realized_pnl

        remaining = held - quantity
        if remaining:
            self.positions[symbol]["quantity"] = remaining
        else:
            del self.positions[symbol]

        trade = self._record_trade(
            "SELL", symbol, quantity, reference_price, fill_price,
            commission, realized_pnl,
            average_cost if remaining else 0.0, **metadata
        )
        trade["net_cash_flow"] = notional - commission
        trade["cost_basis_sold"] = average_cost * quantity
        return trade

    def liquidate(self, symbol, reference_price, **metadata):
        return self.sell(symbol, self.quantity(symbol), reference_price, **metadata)

    def rebalance(self, target_weights, reference_prices, **metadata):
        if any((not math.isfinite(weight) or weight < 0) for weight in target_weights.values()):
            raise ValueError("target weights must be finite and non-negative")
        if sum(target_weights.values()) > 1.0 + 1e-12:
            raise ValueError("target weights must not sum above one")

        equity = self.equity(reference_prices)
        target_quantities = {}
        for symbol, weight in target_weights.items():
            reference_price = float(reference_prices[symbol])
            buy_price = self.cost_model.fill_price("BUY", reference_price)
            all_in_price = buy_price * (1 + self.cost_model.commission_rate)
            target_quantities[symbol] = int((equity * weight) // all_in_price)

        executed = []
        symbols = set(self.positions) | set(target_quantities)
        for symbol in sorted(symbols):
            excess = self.quantity(symbol) - target_quantities.get(symbol, 0)
            if excess > 0:
                executed.append(self.sell(
                    symbol, excess, reference_prices[symbol], **metadata
                ))

        for symbol in target_weights:
            shortage = target_quantities[symbol] - self.quantity(symbol)
            if shortage <= 0:
                continue
            affordable = self.cost_model.max_affordable_quantity(
                self.cash, float(reference_prices[symbol])
            )
            quantity = min(shortage, affordable)
            if quantity > 0:
                executed.append(self.buy(
                    symbol, quantity, reference_prices[symbol], **metadata
                ))
        return executed

    def summary(self, prices):
        closed = [trade for trade in self.trades if trade["action"] == "SELL"]
        wins = sum(trade["realized_pnl"] > 0 for trade in closed)
        losses = sum(trade["realized_pnl"] <= 0 for trade in closed)
        return {
            "cash": self.cash,
            "holdings": self.holdings,
            "positions": {
                symbol: dict(position) for symbol, position in self.positions.items()
            },
            "realized_pnl": self.realized_pnl,
            "unrealized_pnl": self.unrealized_pnl(prices),
            "total_commission": self.total_commission,
            "total_slippage_cost": self.total_slippage_cost,
            "wins": wins,
            "losses": losses,
            "win_rate": wins / len(closed) * 100 if closed else 0.0,
        }

    def _record_trade(self, side, symbol, quantity, reference_price, fill_price,
                      commission, realized_pnl, average_cost_after, **metadata):
        slippage_cost = self.cost_model.slippage_cost(
            side, float(reference_price), fill_price, quantity
        )
        self.total_commission += commission
        self.total_slippage_cost += slippage_cost
        trade = dict(metadata)
        trade.update({
            "action": side,
            "symbol": symbol,
            "price": fill_price,
            "reference_price": float(reference_price),
            "qty": quantity,
            "notional": fill_price * quantity,
            "commission": commission,
            "slippage_cost": slippage_cost,
            "realized_pnl": realized_pnl,
            "average_cost_after": average_cost_after,
            "cash": self.cash,
        })
        self.trades.append(trade)
        return trade
