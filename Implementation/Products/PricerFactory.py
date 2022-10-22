from abc import ABC, abstractmethod
from datetime import date
from typing import List

from Products.Pricer import Pricer
from Products.QuoteProvider import QuoteProvider


class PricerFactory(ABC):
    @abstractmethod
    def createPricer(
        self,
        valuationDate: date,
        underlyings: List[str],
        market: QuoteProvider
    ) -> Pricer:
        pass
