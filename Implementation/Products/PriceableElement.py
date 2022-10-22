from abc import ABC, abstractmethod
from datetime import date

from Products.QuoteProvider import QuoteProvider


class PriceableElement(ABC):
    @abstractmethod
    def getPrice(self, valuationDate: date, market: QuoteProvider) -> float:
        pass
