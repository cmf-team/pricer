from abc import ABC, abstractmethod
from datetime import date
from typing import List


class QuoteProvider(ABC):
    @abstractmethod
    def getQuotes(
        self,
        ticker: str,
        observationDates: List[date]
    ) -> List[float]:
        pass
