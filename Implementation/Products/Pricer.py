from datetime import date

from Products.CashFlow import CashFlow


class Pricer:
    def __init__(self):
        pass

    def getValuationDate(self) -> date:
        pass

    def getDiscountFactor(self, paymentDate: date) -> float:
        pass

    def getCallOptionBasePrice(
        self,
        underlying: str,
        strike: float,
        maturityDate: date
    ) -> float:
        pass

    def getCashFlowBasePrice(self, pricedElement: CashFlow) -> float:
        pass
