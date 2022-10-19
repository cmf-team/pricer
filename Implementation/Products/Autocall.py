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
        maturityDate: date,
        couponDates: List[date],
        couponAmounts: List[float],
        memoryFeature: bool
    ):
        self.__underlyings = underlyings
        self.__couponBarrier = couponBarrier
        self.__autocallBarrier = autocallBarrier
        self.__startDate = startDate
        self.__maturityDate = maturityDate
        self.__couponDates = couponDates
        self.__couponAmounts = couponAmounts
        self.__memoryFeature = memoryFeature

    def getPaymentDates(self) -> list[date]:
        return self.__couponDates

    def getWorstReturns(
        self,
        paymentDate: date,
        market: QuoteProvider
    ) -> numpy.ndarray:
        initialQuotes = numpy.array(
            [
                market.getQuotes(
                    underlying,
                    [self.__startDate]
                )
                for underlying in self.__underlyings
            ]
        )
        paymentDateIndex = self.__couponDates.index(paymentDate)
        quotes = numpy.array(
            [
                market.getQuotes(
                    underlying,
                    self.__couponDates[:paymentDateIndex + 1]
                )
                for underlying in self.__underlyings
            ]
        )
        returns = quotes / initialQuotes
        worstReturns = returns.min(axis=0)
        return worstReturns

    def isRecall(
        self,
        worstReturns: numpy.ndarray,
        paymentDate: date,
    ) -> str:
        if (
                len(worstReturns) > 1 and
                worstReturns[:-1].max() > self.__autocallBarrier
        ):
            return 'Already Recalled'

        if (
                paymentDate == self.__couponDates[-1] or
                worstReturns[-1] > self.__autocallBarrier
        ):
            return 'Recall'

        return 'No'

    def getUnpaidCoupons(
        self,
        worstReturns: List[float]
    ) -> float:
        unpaidCouponsNumber = 0
        for worstReturn in numpy.flip(worstReturns[:-1]):
            if worstReturn < self.__couponBarrier:
                unpaidCouponsNumber += 1
            else:
                break
        return sum(self.__couponAmounts[-unpaidCouponsNumber - 1:-1])

    def getPaymentAmount(
        self,
        paymentDate: date,
        market: QuoteProvider
    ) -> float:
        try:
            paymentDateIndex = self.__couponDates.index(paymentDate)
        except ValueError:
            return 0

        paymentAmount = 0
        worstReturns = self.getWorstReturns(paymentDate, market)

        isRecall = self.isRecall(worstReturns, paymentDate)
        if isRecall == 'Already Recalled':
            return 0
        elif isRecall == 'Recall':
            paymentAmount += 1

        couponCondition = int(worstReturns[-1] >= self.__couponBarrier)
        paymentAmount += (
                couponCondition * self.__couponAmounts[paymentDateIndex]
        )

        if couponCondition and self.__memoryFeature:
            paymentAmount += self.getUnpaidCoupons(worstReturns)

        return paymentAmount

    def getBasePrice(self, valuationDate: date, pricer: Pricer) -> float:
        pass
