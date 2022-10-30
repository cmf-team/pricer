import math
from datetime import date
from typing import List

from numpy import interp
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
            raise ValueError('Nonunique tickres or tenors')

        self.__valuationDate = valuationDate
        self.__durations = self.__tenorToDuration(
            self.__sort(tenors, type='tenors')
        )
        self.__rates = [
            market.getQuotes(
                ticker,
                [self.__valuationDate],
            )[0] / 100 for ticker in self.__sort(tickers, type='tickers')
        ]

    def __sort(self, data, type):
        result = []
        sortOrder = {'D': [], 'W': [], 'M': [], 'Y': []}
        for sample in data:
            sortOrder[sample[-1]].append(sample)

        popKeys = [key for key in sortOrder if len(sortOrder[key]) == 0]
        [sortOrder.pop(key) for key in popKeys]

        for k in sortOrder.keys():
            if type == 'tenors':
                sortOrder[k] = sorted(sortOrder[k], key=lambda x: int(x[:-1]))
            elif type == 'tickers':
                sortOrder[k] = sorted(sortOrder[k], key=lambda x: int(x[4:-1]))
            else:
                raise ValueError('Only tickers and tenors are allowed')

        for durQuotes in sortOrder.items():
            result.extend(durQuotes[1])

        return result

    def getDiscountFactor(self, paymentDate: date) -> float:
        timeToPayment = (paymentDate - self.__valuationDate).days / 365
        rate = 0.

        if timeToPayment >= self.__durations[-1]:
            rate = self.__rates[-1]
        elif timeToPayment < self.__durations[0]:
            rate = self.__rates[0]
        else:
            rate = interp(timeToPayment, self.__durations, self.__rates)

        discountFactor = math.exp(-rate * timeToPayment)
        return discountFactor

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
