import CashFlow
from abc import abstractmethod, ABC
from datetime import date


class Pricer(ABC):
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def getValuationDate(self) -> date:
        pass

    @abstractmethod
    def getDiscountFactor(self, paymentDate: date) -> date:
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
    def CashFlowBasePrice(self, priceElement: CashFlow) -> float:
        pass
