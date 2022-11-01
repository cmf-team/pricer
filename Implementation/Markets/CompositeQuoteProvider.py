from datetime import date
from typing import Iterable
from typing import List

from Products.QuoteProvider import QuoteProvider


class CompositeQuoteProvider(QuoteProvider):
    def init(
        self,
        components: Iterable[QuoteProvider]
    ):
        self.__components = components

    def getQuotes(
        self,
        ticker: str,
        observationDates: List[date]
    ) -> List[float]:
        result = [None] * len(observationDates)
        for component in self.__components:
            componentQuotes = component.getQuotes(ticker, observationDates)
            for quoteIndex in range(len(observationDates)):
                if componentQuotes[quoteIndex] is not None:
                    if result[quoteIndex] is None:
                        result[quoteIndex] = componentQuotes[quoteIndex]
                    else:
                        if result[quoteIndex] != componentQuotes[quoteIndex]:
                            raise ValueError(
                                f"Inconsistent quotes {result[quoteIndex]}"
                                f"and {componentQuotes[quoteIndex]} for "
                                f"{ticker} on {observationDates[quoteIndex]} "
                                f"returned by different components."
                            )
        return result
