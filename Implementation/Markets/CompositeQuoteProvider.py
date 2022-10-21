from Products.QuoteProvider import QuoteProvider
from typing import Iterable, List
from datetime import date


class CompositeQuoteProvider(QuoteProvider):
    def __init__(
        self,
        components: Iterable[QuoteProvider]
    ):
        self.__components = components

    def getQuotes(
        self,
        ticker: str,
        observationDates: List[date]
    ) -> List[float]:
        for component in self.__components:
            if component.getQuotes(
                ticker, observationDates
            ) == component.getQuotes(
                ticker, observationDates
            ):
                return component.getQuotes(
                    ticker, observationDates
                )
            else:
                raise ValueError
