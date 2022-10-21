from datetime import date
from unittest import TestCase

from Products.Autocall import Autocall
from Products.QuoteProvider import QuoteProvider

GAZPQuotes = {
    date(2022, 9, 1): 100,
    date(2022, 10, 1): 105,
    date(2022, 11, 1): 101,
    date(2022, 12, 1): 106,
}

YNDXQuotes = {
    date(2022, 9, 1): 150,
    date(2022, 10, 1): 130,
    date(2022, 11, 1): 155,
    date(2022, 12, 1): 155,
}


class QuoteProviderStub(QuoteProvider):
    def __init__(self):
        pass

    def getQuotes(
        self,
        ticker: str,
        observationDates: list[date]
    ) -> list[float]:

        if ticker == "GAZP":
            try:
                return [
                    GAZPQuotes.get(observationDate) for
                    observationDate in observationDates
                ]
            except KeyError:
                raise NotImplementedError()

        if ticker == "YNDX":
            try:
                return [
                    YNDXQuotes.get(observationDate) for
                    observationDate in observationDates
                ]
            except KeyError:
                raise NotImplementedError()


class AutocallTest(TestCase):
    def setUp(self) -> None:
        self.__testedNoMemoryMonthly = Autocall(
            underlyings=['GAZP', 'YNDX'],
            couponBarrier=1,
            autocallBarrier=1.1,
            startDate=date(2022, 9, 1),
            maturityDate=date(2022, 12, 1),
            couponDates=[
                date(2022, 10, 1), date(2022, 11, 1), date(2022, 12, 1)
            ],
            couponAmounts=[0.1 * 30 / 365, 0.1 * 31 / 365, 0.1 * 30 / 365],
            memoryFeature=False
        )

        self.__testedNoMemoryQuarterly = Autocall(
            underlyings=['GAZP', 'YNDX'],
            couponBarrier=1,
            autocallBarrier=1.1,
            startDate=date(2022, 9, 1),
            maturityDate=date(2022, 12, 1),
            couponDates=[date(2022, 12, 1)],
            couponAmounts=[0.1 * 91 / 365],
            memoryFeature=False
        )

        self.__testedMemoryMonthly = Autocall(
            underlyings=['GAZP', 'YNDX'],
            couponBarrier=1,
            autocallBarrier=1,
            startDate=date(2022, 9, 1),
            maturityDate=date(2022, 12, 1),
            couponDates=[
                date(2022, 10, 1), date(2022, 11, 1), date(2022, 12, 1)
            ],
            couponAmounts=[0.2 * 30 / 365, 0.2 * 31 / 365, 0.2 * 30 / 365],
            memoryFeature=True
        )

    def testZeroCouponNoMemory(self):
        sampleMarket = QuoteProviderStub()
        self.assertEqual(
            0,
            self.__testedNoMemoryMonthly.getPaymentAmount(
                date(2022, 10, 1),
                sampleMarket
            )
        )

    def testNonZeroCouponNoMemory(self):
        sampleMarket = QuoteProviderStub()
        with self.subTest():
            self.assertAlmostEqual(
                0.1 * (date(2022, 11, 1) - date(2022, 10, 1)).days / 365,
                self.__testedNoMemoryMonthly.getPaymentAmount(
                    date(2022, 11, 1),
                    sampleMarket
                )
            )
        with self.subTest():
            self.assertAlmostEqual(
                1 + 0.1 * (date(2022, 12, 1) - date(2022, 11, 1)).days / 365,
                self.__testedNoMemoryMonthly.getPaymentAmount(
                    date(2022, 12, 1),
                    sampleMarket
                )
            )

    def testNonZeroCouponNoMemoryQuarterly(self):
        sampleMarket = QuoteProviderStub()
        self.assertAlmostEqual(
            1 + 0.1 * (date(2022, 12, 1) - date(2022, 9, 1)).days / 365,
            self.__testedNoMemoryQuarterly.getPaymentAmount(
                date(2022, 12, 1),
                sampleMarket
            ),
        )

    def testMemoryFeature(self):
        sampleMarket = QuoteProviderStub()
        self.assertAlmostEqual(
            (1 + 0.2 * (date(2022, 10, 1) - date(2022, 9, 1)).days / 365 +
             0.2 * (date(2022, 11, 1) - date(2022, 10, 1)).days / 365),
            self.__testedMemoryMonthly.getPaymentAmount(
                date(2022, 11, 1),
                sampleMarket
            )
        )
