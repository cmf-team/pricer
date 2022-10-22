from abc import ABC, abstractmethod
from datetime import date


class DiscountCurve(ABC):
    @abstractmethod
    def getValuationDate(self) -> date:
        pass

    @abstractmethod
    def getDiscountFactor(self, paymentDate: date) -> float:
        pass
