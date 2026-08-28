import math


class ExecutionCostModel:
    def __init__(self, commission_rate=0.0, slippage_bps=0.0):
        if not math.isfinite(commission_rate) or commission_rate < 0:
            raise ValueError("commission_rate는 0 이상의 유한한 값이어야 합니다.")

        if not math.isfinite(slippage_bps) or slippage_bps < 0:
            raise ValueError("slippage_bps는 0 이상의 유한한 값이어야 합니다.")

        self.commission_rate = commission_rate
        self.slippage_bps = slippage_bps

    def fill_price(self, side, reference_price):
        if not math.isfinite(reference_price) or reference_price <= 0:
            raise ValueError("기준 가격은 양수인 유한한 값이어야 합니다.")

        slippage_rate = self.slippage_bps / 10000

        if side == "BUY":
            return reference_price * (1 + slippage_rate)

        if side == "SELL":
            return reference_price * (1 - slippage_rate)

        raise ValueError("side는 BUY 또는 SELL이어야 합니다.")

    def commission(self, notional):
        return notional * self.commission_rate

    def max_affordable_quantity(self, cash, reference_price):
        fill_price = self.fill_price("BUY", reference_price)
        cash_per_share = fill_price * (1 + self.commission_rate)
        return max(0, int(cash // cash_per_share))

    @staticmethod
    def slippage_cost(side, reference_price, fill_price, quantity):
        if side == "BUY":
            return (fill_price - reference_price) * quantity

        return (reference_price - fill_price) * quantity
