from abc import ABC, abstractmethod
from datetime import date
from typing import List

from Products.QuoteProvider import QuoteProvider


class CashFlow(ABC):
    @abstractmethod
    def getPaymentDates(self) -> List[date]:
        pass

    @abstractmethod
    def getPaymentAmount(
        self,
        paymentDate: date,
        market: QuoteProvider
    ) -> float:
        pass
