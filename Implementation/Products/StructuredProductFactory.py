from datetime import date
from enum import Enum
from typing import List

from dateutil.rrule import MONTHLY, rrule

from Products.Autocall import Autocall


class ObservationsFrequency(Enum):
    MONTHLY = 1
    QUARTERLY = 3
    SEMIANNUAL = 6
    ANNUAL = 12


class StructuredProductFactory:
    @staticmethod
    def createAutocall(
        underlyings: List[str],
        couponBarrier: float,
        autocallBarrier: float,
        startDate: date,
        maturityDate: date,
        observationsFrequency: ObservationsFrequency,
        annulizedCouponLevel: float,
        memoryFeature: bool
    ):
        if autocallBarrier < couponBarrier:
            raise ValueError(
                'Autocall barrier must be greater than or equal '
                'to a coupon barrier.'
            )

        couponDates = [
            dt.date() for dt in rrule(
                MONTHLY,
                interval=observationsFrequency.value,
                dtstart=startDate,
                until=maturityDate
            )
        ][1:]

        if len(couponDates) == 0:
            raise ValueError(
                'There are no payment dates according to the '
                'entered data. Check startDate, maturityDate and '
                'observationsFrequency.'
            )

        couponAmount = (annulizedCouponLevel / 12 *
                        observationsFrequency.value)
        couponAmounts = [couponAmount for _ in range(len(couponDates))]

        return Autocall(
            underlyings=underlyings,
            couponBarrier=couponBarrier,
            autocallBarrier=autocallBarrier,
            startDate=startDate,
            maturityDate=maturityDate,
            couponDates=couponDates,
            couponAmounts=couponAmounts,
            memoryFeature=memoryFeature
        )
