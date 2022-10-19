from datetime import date
from enum import Enum
from typing import List

import numpy
from dateutil.rrule import MONTHLY, rrule

from Products.CashFlow import CashFlow
from Products.Pricer import Pricer
from Products.QuoteProvider import QuoteProvider


class ObservationsFrequency(Enum):
    MONTHLY = 1
    QUARTERLY = 3
    SEMIANNUAL = 6
    ANNUAL = 12


class Autocall(CashFlow):
    def __init__(
        self,
        underlyings: List[str],
        couponBarrier: float,
        autocallBarrier: float,
        startDate: date,
        maturityDate: date,
        observationsFrequency: ObservationsFrequency,
        annulizedCouponLevel: float,
        memoryFeature: bool
    ):
        self.__startDate = startDate
        self.__maturityDate = maturityDate
        self.__observationsFrequency = observationsFrequency
        self.__underlyings = underlyings
        self.__couponLevel = annulizedCouponLevel / 12 * \
                             observationsFrequency.value
        self.__autocallBarrier = autocallBarrier
        self.__couponBarrier = couponBarrier
        self.__allDates = [
            dt.date() for dt in rrule(
                MONTHLY,
                interval=self.__observationsFrequency.value,
                dtstart=self.__startDate,
                until=self.__maturityDate
            )
        ]
        if memoryFeature and autocallBarrier == couponBarrier:
            self.__memoryFeature = "AutocallIncremental"
        elif memoryFeature and autocallBarrier != couponBarrier:
            self.__memoryFeature = "PhoenixMemory"
        else:
            self.__memoryFeature = None

        if self.__autocallBarrier < self.__couponBarrier:
            raise ValueError(
                'Autocall barrier must be greater than or equal '
                'to a coupon barrier.'
            )

        if len(self.__allDates) <= 1:
            raise ValueError(
                'There are no payment dates according to the '
                'entered data. Check startDate, maturityDate and '
                'observationsFrequency.'
            )

    def getPaymentDates(self) -> list[date]:
        return self.__allDates[1:]

    def getPaymentAmount(
        self,
        paymentDate: date,
        market: QuoteProvider
    ) -> float:
        if paymentDate not in self.__allDates[1:]:
            return 0

        paymentDateIndex = self.__allDates.index(paymentDate)
        quotes = numpy.array(
            [
                market.getQuotes(
                    underlying,
                    self.__allDates[:paymentDateIndex + 1]
                )
                for underlying in self.__underlyings
            ]
        )
        normalizedQuotes = quotes / quotes[:, 0][:, None]
        worstOfNormalizedQuotes = normalizedQuotes[:, 1:].min(axis=0)

        if len(worstOfNormalizedQuotes) == 1:
            alreadyAutocalled = 0
        else:
            alreadyAutocalled = (
                    worstOfNormalizedQuotes[:-1].max() >
                    self.__autocallBarrier
            )
        if alreadyAutocalled:
            return 0

        couponCondition = int(
            worstOfNormalizedQuotes[-1] >=
            self.__couponBarrier
        )

        if couponCondition and self.__memoryFeature == "AutocallIncremental":
            return 1 + len(
                worstOfNormalizedQuotes
            ) * self.__couponLevel
        elif couponCondition and self.__memoryFeature == "PhoenixMemory":
            unpaidCouponsNumber = 0
            i = len(worstOfNormalizedQuotes[:-1]) - 1
            while (
                    i >= 0 and
                    worstOfNormalizedQuotes[:-1][i] < self.__couponBarrier
            ):
                unpaidCouponsNumber += 1
                i -= 1

            coupon = unpaidCouponsNumber * self.__couponLevel
        elif couponCondition and not self.__memoryFeature:
            coupon = self.__couponLevel
        else:
            coupon = 0

        if paymentDateIndex == len(self.__allDates) - 1:
            autocallCondition = 1
        else:
            autocallCondition = int(
                worstOfNormalizedQuotes[-1] >=
                self.__autocallBarrier
            )

        return coupon + autocallCondition

    def getBasePrice(self, valuationDate: date, pricer: Pricer) -> float:
        pass
