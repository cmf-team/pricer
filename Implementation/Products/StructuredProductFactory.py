from datetime import date
from enum import Enum
from typing import List

from dateutil.rrule import MONTHLY, rrule

from Products.Autocall import Autocall


class CouponFrequency(Enum):
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
        couponFrequency: CouponFrequency,
        couponCount: int,
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
                interval=couponFrequency.value,
                dtstart=startDate,
                count=couponCount + 1
            )
        ]

        couponAmounts = [
            couponRate * (couponDates[i + 1] - couponDates[i]).days / 365
            for i in range(len(couponDates) - 1)
        ]

        return Autocall(
            underlyings=underlyings,
            couponBarrier=couponBarrier,
            autocallBarrier=autocallBarrier,
            startDate=startDate,
            couponDates=couponDates[1:],
            couponAmounts=couponAmounts,
            memoryFeature=memoryFeature
        )
