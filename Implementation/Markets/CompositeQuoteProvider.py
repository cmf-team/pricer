from Products.QuoteProvider import QuoteProvider
from typing import Iterable, List
from datetime import date


class CompositeQuoteProvider(QuoteProvider):
    def init(self, components: Iterable[QuoteProvider]):
        self.__components = components

    def getQuotes(self, ticker: str, observationDates: List[date]) -> List[float]:
        for component in self.__components:
            quote = component.getQuotes(ticker, observationDates)
