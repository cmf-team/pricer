import math
from datetime import date
from typing import List

from Products.DiscountCurve import DiscountCurve
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
            i[0] / 100 for i in
            [market.getQuotes(
                ticker,
                [self.__valuationDate],
            ) for ticker in tickers]
        ]

    def getDiscountFactor(self, paymentDate: date) -> float:
        timeToPayment = (paymentDate - self.__valuationDate).days / 365
        rate = 0.

        if len(self.__durations) == 1:
            rate = self.__rates[0]
        elif timeToPayment >= self.__durations[-1]:
            rate = self.__interpolate(timeToPayment, len(self.__durations) - 2)
        else:
            for i in range(1, len(self.__durations)):
                if timeToPayment < self.__durations[i]:
                    rate = self.__interpolate(timeToPayment, i - 1)
                    break

        discontFactor = math.exp(-rate*timeToPayment)
        return discontFactor

    def __interpolate(self, timeToPayment: float, ratePosition: int) -> float:
        result = (
            self.__rates[ratePosition] +
            (timeToPayment - self.__durations[ratePosition]) *
            (
                (
                    self.__rates[ratePosition + 1] -
                    self.__rates[ratePosition]
                ) /
                (
                    self.__durations[ratePosition + 1] -
                    self.__durations[ratePosition]
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
