import math
from datetime import date
from typing import List, Optional

from Simulation.DiscountCurve import DiscountCurve
from Products.QuoteProvider import QuoteProvider


class IndexDiscountCurve(DiscountCurve):
    def __init__(
        self,
        valuationDate: date,
        tenors: List[str],
        tickers: List[str],
        market: QuoteProvider
    ) -> None:
        self.__valuationDate = valuationDate
        self.__durations = self.__tenorToDuration(tenors)
        self.__rates = [
            market.getQuotes(
                ticker,
                [self.__valuationDate],
            )[0] / 100 for ticker in tickers
        ]

    def getDiscountFactor(self, paymentDate: date) -> float:
        timeToPayment = (paymentDate - self.__valuationDate).days / 365
        rate = 0.

        if len(self.__durations) == 1:
            rate = self.__rates[0]
        elif timeToPayment >= self.__durations[-1]:
            rate = self.__interpolate(timeToPayment, extrapolate=True)
        else:
            for i in range(1, len(self.__durations)):
                if timeToPayment < self.__durations[i]:
                    rate = self.__interpolate(timeToPayment, i - 1)
                    break

        discountFactor = math.exp(-rate * timeToPayment)
        return discountFactor

    def __interpolate(
        self,
        timeToPayment: float,
        ratePosition: Optional[int] = None,
        extrapolate: bool = False,
    ) -> float:
        if extrapolate:
            firstPoint = 0
            lastPoint = len(self.__rates) - 1
        else:
            firstPoint = ratePosition
            lastPoint = ratePosition + 1

        result = (
            self.__rates[firstPoint] +
            (timeToPayment - self.__durations[firstPoint]) *
            (
                (
                    self.__rates[lastPoint] -
                    self.__rates[firstPoint]
                ) /
                (
                    self.__durations[lastPoint] -
                    self.__durations[firstPoint]
                )
            )
        )

        return result

    def __tenorToDuration(self, tenors: List[str]) -> List:
        durations = []
        for tenor in tenors:
            if tenor.endswith('D'):
                durations.append(int(tenor[:-1]) / 365)
            elif tenor.endswith('W'):
                durations.append(int(tenor[:-1]) * 7 / 365)
            elif tenor.endswith('M'):
                durations.append(int(tenor[:-1]) * 30 / 365)
            elif tenor.endswith('Y'):
                durations.append(int(tenor[:-1]))
        return durations

    def getValuationDate(self) -> date:
        return self.__valuationDate
