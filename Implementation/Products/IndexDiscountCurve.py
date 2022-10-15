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
        self.__durations = self.tenorsToAct(tenors)
        self.__rates = [
            i[0] / 100 for i in
            [market.getQuotes(ticker, [self.__valuationDate]) for ticker in tickers]
        ]

    def getDiscountFactor(self, paymentDate: date) -> float:
        timeToPayment = (paymentDate - self.__valuationDate).days / 365
        rate = 0
        for i in range(len(self.__durations)):
            if timeToPayment > self.__durations[i] or len(self.__durations) == 1:
                rate = self.__interpolate(timeToPayment, i)
                break

        discontFactor = math.exp(-rate*timeToPayment)
        return discontFactor

    def __interpolate(self, timeToPayment: float, rate_position: int) -> float:
        if rate_position < len(self.__rates) - 1 and len(self.__rates) > 1:
            output = (
                self.__rates[rate_position] +
                (timeToPayment - self.__durations[rate_position]) *
                (
                    (self.__rates[rate_position+1] - self.__rates[rate_position]) /
                    (
                        self.__durations[rate_position+1] -
                        self.__durations[rate_position]
                    )
                )
            )
        elif rate_position >= len(self.__rates) - 1 and len(self.__rates) > 1:
            output = self.__rates[-1] + (timeToPayment - self.__durations[-1]) * (
                (self.__rates[-2] - self.__rates[-1]) /
                (self.__durations[-2] - self.__durations[-1])
            )
        elif len(self.__rates) == 1:
            output = self.__rates[0]
        return output

    def tenorsToAct(self, durations: List[str]) -> List:
        act_durations = []
        for duration in durations:
            if duration.endswith('D'):
                act_durations.append(int(duration[:-1]) / 365)
            elif duration.endswith('W'):
                act_durations.append(int(duration[:-1]) * 7 / 365)
            elif duration.endswith('M'):
                act_durations.append(int(duration[:-1]) * 30 / 365)
            elif duration.endswith('Y'):
                act_durations.append(int(duration[:-1]))
        return act_durations

    def getValuationDate(self) -> date:
        return self.__valuationDate
