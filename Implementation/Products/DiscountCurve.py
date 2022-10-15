from abc import ABC, abstractmethod
from datetime import date


class DiscountCurve(ABC):
    @abstractmethod
    def getDiscountFactor(self, paymentDate: date):
        pass

    @abstractmethod
    def getValuationDate(self) -> date:
        pass
