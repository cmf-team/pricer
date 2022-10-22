from datetime import date
from abc import ABC, abstractmethod

from Products.CashFlow import CashFlow


class Pricer(ABC):
    @abstractmethod
    def getValuationDate(self) -> date:
        pass

    @abstractmethod
    def getDiscountFactor(self, paymentDate: date) -> float:
        pass

    @abstractmethod
    def getCallOptionBasePrice(
        self,
        underlying: str,
        strike: float,
        maturityDate: date
    ) -> float:
        pass

    @abstractmethod
    def getCashFlowBasePrice(self, pricedElement: CashFlow) -> float:
        pass
