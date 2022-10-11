import abc
import math
from datetime import date
from typing import List

from QuoteProvider import QuoteProvider


class DiscountCurve(abc.ABC):
    def __init__(
        self,
        valuationDate: date,
        tenors: List[str],
        tickers: List[str],
        market: QuoteProvider
    ) -> None:
        super().__init__()
        pass
    
    @abc.abstractmethod
    def getDiscountFactor(self):
        """Get discont factor for a certain date"""

    @abc.abstractmethod
    def get_valuationDate(self) -> date:
        """Get valuation date"""


class IndexDiscountCurve(DiscountCurve):
    def __init__(
        self,
        valuationDate: date,
        tenors: List[str],
        tickers: List[str],
        market: QuoteProvider
    ) -> None:
        super().__init__(
            valuationDate,
            tenors,
            tickers,
            market,
        )
        self.valuationDate = valuationDate
        self.durations = self.tenorsToAct(tenors)
        self.rates = [i[0] / 100 for i in [market.getQuotes(ticker, [valuationDate]) for ticker in tickers]]
    

    def getDiscountFactor(self, paymentDate: date):
        t = (paymentDate - self.valuationDate).days / 365
        rate = 0
        for i in range(len(self.durations)):
            if t > self.durations[i] or len(self.durations) == 1:
                rate = self.interpolate(t, i)
                break

        discontFactor = math.exp(-rate*t)
        return discontFactor
    
    def interpolate(self, t, i):
        if i < len(self.rates) - 1 and len(self.rates) > 1:
            output = self.rates[i] + (t - self.durations[i]) * (
                (self.rates[i+1] - self.rates[i])/
                (self.durations[i+1] - self.durations[i])
            )
        elif i >= len(self.rates) - 1 and len(self.rates) > 1:
            output = self.rates[-1] + (t - self.durations[-1]) * (
                (self.rates[-2] - self.rates[-1])/
                (self.durations[-2] - self.durations[-1])
            )
        elif len(self.rates) == 1:
            output = self.rates[0]
        return output

    def tenorsToAct(self, durations) -> List:
        act_durations = []
        for duration in durations:
            if duration[-1] == 'D':
                act_durations.append(int(duration[:-1])/365)
            elif duration[-1] == 'W':
                act_durations.append(int(duration[:-1]) * 7 /365)
            elif duration[-1] == 'M':
                act_durations.append(int(duration[:-1]) * 30 /365)
            elif duration[-1] == 'Y':
                act_durations.append(int(duration[:-1]))
        return act_durations

    def get_valuationDate(self) -> date:
        return self.valuationDate
