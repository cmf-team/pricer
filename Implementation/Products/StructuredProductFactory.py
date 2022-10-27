from datetime import date
from enum import Enum
from typing import List

from dateutil.rrule import MONTHLY, rrule

from Products.Autocall import Autocall


class PaymentFrequency(Enum):
    MONTHLY: int = 1
    QUARTERLY: int = 3
    SEMIANNUAL: int = 6
    ANNUAL: int = 12


class StructuredProductFactory:
    @staticmethod
    def createAutocall(
        underlyings: List[str],
        couponBarrier: float,
        autocallBarrier: float,
        startDate: date,
        maturityDate: date,
        paymentFrequency: PaymentFrequency,
        couponRate: float,
        memoryFeature: bool
    ):
        if autocallBarrier < couponBarrier:
            raise ValueError(
                'Autocall barrier must be greater than or equal '
                'to a coupon barrier.'
            )

        couponDates = [
            couponDate.date() for couponDate in rrule(
                MONTHLY,
                interval=paymentFrequency.value,
                dtstart=startDate,
                until=maturityDate
            )
        ]

        if len(couponDates) <= 1:
            raise ValueError(
                'There are no payment dates according to the '
                'entered data. Check startDate, maturityDate and '
                'observationsFrequency.'
            )

        couponAmounts = [
            couponRate * (couponDates[i + 1] - couponDates[i]).days / 365
            for i in range(len(couponDates) - 1)
        ]

        return Autocall(
            underlyings=underlyings,
            couponBarrier=couponBarrier,
            autocallBarrier=autocallBarrier,
            startDate=startDate,
            maturityDate=maturityDate,
            couponDates=couponDates[1:],
            couponAmounts=couponAmounts,
            memoryFeature=memoryFeature
        )
