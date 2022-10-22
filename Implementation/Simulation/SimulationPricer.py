from datetime import date
from math import log, sqrt
from typing import List

from scipy.stats import norm

from Products.CashFlow import CashFlow
from Products.Pricer import Pricer
from Products.QuoteProvider import QuoteProvider
from Simulation.CovarianceTermStructure import CovarianceTermStructure
from Simulation.DiscountCurve import DiscountCurve


class SimulationPricer(Pricer):
    def __init__(
        self,
        underlyings: List[str],
        valuationDate: date,
        originalMarket: QuoteProvider,
        discountCurve: DiscountCurve,
        underlyingCovarianceForecast: CovarianceTermStructure
    ):
        self.__underlyings = underlyings
        self.__valuationDate = valuationDate
        self.__originalMarket = originalMarket
        self.__discountCurve = discountCurve
        self.__underlyingCovarianceForecast = underlyingCovarianceForecast

    def getValuationDate(self) -> date:
        return self.__valuationDate

    def getDiscountFactor(self, paymentDate: date) -> float:
        return self.__discountCurve.getDiscountFactor(paymentDate)

    def getCallOptionBasePrice(
        self,
        underlying: str,
        strike: float,
        maturityDate: date
    ) -> float:
        undelyingIndex = self.__underlyings.index(underlying)
        totalVariance = \
            self.__underlyingCovarianceForecast.getTotalCovariance(
                maturityDate
            )[undelyingIndex, undelyingIndex]
        spotPrice = self.__originalMarket.getQuotes(
            ticker=underlying,
            observationDates=[self.__valuationDate]
        )[0]
        discountFactor = self.getDiscountFactor(self.__valuationDate)
        forwardPrice = spotPrice / discountFactor
        d1 = (log(forwardPrice / strike) + totalVariance / 2) / sqrt(
            totalVariance
        )
        d2 = (log(forwardPrice / strike) - totalVariance / 2) / sqrt(
            totalVariance
        )
        return discountFactor * (
                forwardPrice * norm.cdf(d1) - strike * norm.cdf(d2))

    def getCashFlowBasePrice(self, pricedElement: CashFlow) -> float:
        pass
