from Products.QuoteProvider import QuoteProvider
from typing import List, Iterable
from datetime import date


class CompositeQuoteProvider(QuoteProvider):
    def __init__(
        self,
        components: Iterable[QuoteProvider]
    ) -> None:
        self.components = components

    def getQuotes(
        self,
        ticker: str,
        observationDates: List[date]
    ) -> List[float]:
        for component in range(len(self.components) - 1):
            if self.components[component].getQuotes(
                ticker, observationDates
            ) == self.components[component].getQuotes(
                ticker, observationDates
            ):
                return self.components[component].getQuotes(
                    ticker, observationDates
                )
            else:
                raise ValueError
