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

    def getPaymentDates(self) -> List[date]:
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

    def __isRecalled(
        self,
        worstReturns: numpy.ndarray,
        couponDate: date,
    ) -> str:
        if (
                len(worstReturns) > 1 and
                worstReturns[:-1].max() > self.__autocallBarrier
        ):
            return 'Already Recalled'

        if (
                couponDate == self.__couponDates[-1] or
                worstReturns[-1] > self.__autocallBarrier
        ):
            return 'Recall'

        return 'No'

    def getUnpaidCoupons(
        self,
        worstReturns: List[float],
        couponCondition: bool,
    ) -> float:
        if not couponCondition or not self.__memoryFeature:
            return 0

        unpaidCouponsAmount = 0
        for i in range(len(worstReturns) - 2, -1, -1):
            if worstReturns[i] < self.__couponBarrier:
                unpaidCouponsAmount += self.__couponAmounts[i]
            else:
                break

        return unpaidCouponsAmount

    def getPaymentAmount(
        self,
        paymentDate: date,
        market: QuoteProvider
    ) -> float:
        if paymentDate in self.__couponDates:
            paymentDateIndex = self.__couponDates.index(paymentDate)
        else:
            return 0

        paymentAmount = 0
        worstReturns = self.getWorstReturns(paymentDate, market)

        isRecall = self.__isRecalled(worstReturns, paymentDate)
        if isRecall == 'Already Recalled':
            return 0
        elif isRecall == 'Recall':
            paymentAmount += 1

        if worstReturns[-1] >= self.__couponBarrier:
            couponCondition = True
        else:
            couponCondition = False

        paymentAmount += (
                couponCondition * self.__couponAmounts[paymentDateIndex]
        )
        paymentAmount += self.getUnpaidCoupons(worstReturns, couponCondition)

        return paymentAmount

    def getBasePrice(self, valuationDate: date, pricer: Pricer) -> float:
        pass
