import math
from abc import ABC, abstractmethod
from datetime import date
from typing import List

from Products.QuoteProvider import QuoteProvider


class DiscountCurve(ABC):
    @abstractmethod
    def getDiscountFactor(self, paymentDate: date):
        pass

    @abstractmethod
    def get_valuationDate(self) -> date:
        pass


class IndexDiscountCurve(DiscountCurve):
    def __init__(
        self,
        valuationDate: date,
        tenors: List[str],
        tickers: List[str],
        market: QuoteProvider
    ) -> None:
        self.valuationDate = valuationDate
        self.durations = self.tenorsToAct(tenors)
        self.rates = [
            i[0] / 100 for i in
            [market.getQuotes(ticker, [valuationDate]) for ticker in tickers]
        ]

    def getDiscountFactor(self, paymentDate: date) -> float:
        timeToPayment = (paymentDate - self.valuationDate).days / 365
        rate = 0
        for i in range(len(self.durations)):
            if timeToPayment > self.durations[i] or len(self.durations) == 1:
                rate = self.__interpolate(timeToPayment, i)
                break

        discontFactor = math.exp(-rate*timeToPayment)
        return discontFactor

    def __interpolate(self, timeToPayment: float, rate_position: int) -> float:
        if rate_position < len(self.rates) - 1 and len(self.rates) > 1:
            output = (
                self.rates[rate_position] +
                (timeToPayment - self.durations[rate_position]) *
                (
                    (self.rates[rate_position+1] - self.rates[rate_position]) /
                    (
                        self.durations[rate_position+1] -
                        self.durations[rate_position]
                    )
                )
            )
        elif rate_position >= len(self.rates) - 1 and len(self.rates) > 1:
            output = self.rates[-1] + (timeToPayment - self.durations[-1]) * (
                (self.rates[-2] - self.rates[-1]) /
                (self.durations[-2] - self.durations[-1])
            )
        elif len(self.rates) == 1:
            output = self.rates[0]
        return output

    def tenorsToAct(self, durations: List[str]) -> List:
        act_durations = []
        for duration in durations:
            if duration[-1] == 'D':
                act_durations.append(int(duration[:-1]) / 365)
            elif duration[-1] == 'W':
                act_durations.append(int(duration[:-1]) * 7 / 365)
            elif duration[-1] == 'M':
                act_durations.append(int(duration[:-1]) * 30 / 365)
            elif duration[-1] == 'Y':
                act_durations.append(int(duration[:-1]))
        return act_durations

    def get_valuationDate(self) -> date:
        return self.valuationDate
