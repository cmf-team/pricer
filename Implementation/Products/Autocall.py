from datetime import date
from typing import List

import numpy

from Products.CashFlow import CashFlow
from Products.Pricer import Pricer
from Products.QuoteProvider import QuoteProvider


class Autocall(CashFlow):
    def __init__(
        self,
        underlyings: List[str],
        couponBarrier: float,
        autocallBarrier: float,
        startDate: date,
        couponDates: List[date],
        couponAmounts: List[float],
        memoryFeature: bool
    ):
        self.__underlyings = underlyings
        self.__couponBarrier = couponBarrier
        self.__autocallBarrier = autocallBarrier
        self.__startDate = startDate
        self.__couponDates = couponDates
        self.__couponAmounts = couponAmounts
        self.__memoryFeature = memoryFeature

    def getPaymentDates(self) -> List[date]:
        return self.__couponDates

    def __getWorstReturn(
        self,
        paymentDate: date,
        market: QuoteProvider
    ) -> float:
        quotes = numpy.array(
            [
                market.getQuotes(
                    underlying,
                    [self.__startDate, paymentDate]
                )
                for underlying in self.__underlyings
            ]
        )
        returns = quotes[:, 1] / quotes[:, 0]
        return returns.min()

    def __isAutocallBarrierHit(
        self,
        couponDate: date,
        market: QuoteProvider
    ) -> bool:
        worstReturn = self.__getWorstReturn(couponDate, market)
        return worstReturn > self.__autocallBarrier

    def __getMemorizedCoupons(
        self,
        paymentDate: date,
        market: QuoteProvider
    ) -> float:
        if not self.__memoryFeature:
            return 0

        memorizedCoupons = 0
        paymentDateIndex = self.__couponDates.index(paymentDate)
        for couponDateIndex in range(paymentDateIndex - 1, -1, -1):
            couponDate = self.__couponDates[couponDateIndex]
            worstReturn = self.__getWorstReturn(couponDate, market)
            if worstReturn < self.__couponBarrier:
                memorizedCoupons += self.__couponAmounts[couponDateIndex]
            else:
                break
        return memorizedCoupons

    def getPaymentAmount(
        self,
        paymentDate: date,
        market: QuoteProvider
    ) -> float:
        if paymentDate in self.__couponDates:
            paymentDateIndex = self.__couponDates.index(paymentDate)
        else:
            return 0

        for couponDateIndex in range(paymentDateIndex):
            if self.__isAutocallBarrierHit(
                self.__couponDates[couponDateIndex],
                market
            ):
                return 0

        paymentAmount = 0
        if (
            paymentDate == self.__couponDates[-1] or
            self.__isAutocallBarrierHit(
                self.__couponDates[paymentDateIndex],
                market
            )
        ):
            paymentAmount += 1

        if self.__getWorstReturn(paymentDate, market) >= self.__couponBarrier:
            paymentAmount += self.__couponAmounts[paymentDateIndex]
            paymentAmount += self.__getMemorizedCoupons(paymentDate, market)

        return paymentAmount

    def getBasePrice(self, valuationDate: date, pricer: Pricer) -> float:
        pass
