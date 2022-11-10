import math
from datetime import date
from typing import List

import numpy as np
from Products.QuoteProvider import QuoteProvider
from Simulation.DiscountCurve import DiscountCurve


class IndexDiscountCurve(DiscountCurve):
    def __init__(
        self,
        valuationDate: date,
        tenors: List[str],
        tickers: List[str],
        market: QuoteProvider
    ) -> None:
        if (
            len(set(tenors)) != len(tenors) or
            len(set(tickers)) != len(tickers)
        ):
            raise ValueError('Nonunique tickres or tenors or length mismatch')

        self.__durations = self.__tenorToDuration(tenors)
        sortOrder = np.argsort(self.__durations).tolist()
        sortedTickers = [
            tickers[sortOrder.index(i)] for i in range(len(sortOrder))
        ]
        self.__durations = sorted(self.__durations)

        self.__valuationDate = valuationDate
        self.__rates = [
            market.getQuotes(
                ticker,
                [self.__valuationDate],
            )[0] / 100 for ticker in sortedTickers
        ]

    def getDiscountFactor(self, paymentDate: date) -> float:
        timeToPayment = (paymentDate - self.__valuationDate).days / 365

        if timeToPayment >= self.__durations[-1]:
            rate = self.__rates[-1]
        elif timeToPayment < self.__durations[0]:
            rate = self.__rates[0]
        else:
            rate = np.interp(timeToPayment, self.__durations, self.__rates)

        return math.exp(-rate * timeToPayment)

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
            else:
                raise ValueError('Unknown tenor.')
        return durations

    def getValuationDate(self) -> date:
        return self.__valuationDate
