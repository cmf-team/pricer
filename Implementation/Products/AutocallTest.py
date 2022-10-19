from datetime import date
from unittest import TestCase

from Products.QuoteProvider import QuoteProvider
from Products.StructuredProductFactory import ObservationsFrequency, \
    StructuredProductFactory

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
        self.__NoMemoryMonthly = {
            'underlyings': ['GAZP', 'YNDX'],
            'couponBarrier': 1,
            'autocallBarrier': 1.1,
            'startDate': date(2022, 9, 1),
            'maturityDate': date(2022, 12, 1),
            'observationsFrequency': ObservationsFrequency.MONTHLY,
            'annulizedCouponLevel': 0.1,
            'memoryFeature': False
        }
        self.__NoMemoryQuarterly = {
            'underlyings': ['GAZP', 'YNDX'],
            'couponBarrier': 1,
            'autocallBarrier': 1.1,
            'startDate': date(2022, 9, 1),
            'maturityDate': date(2022, 12, 1),
            'observationsFrequency': ObservationsFrequency.QUARTERLY,
            'annulizedCouponLevel': 0.1,
            'memoryFeature': False
        }
        self.__testedNoMemoryMonthly = \
            StructuredProductFactory.createAutocall(**self.__NoMemoryMonthly)
        self.__testedNoMemoryQuarterly = \
            StructuredProductFactory.createAutocall(**self.__NoMemoryQuarterly)

    def testExceptions(self):
        with self.assertRaisesRegex(ValueError, 'barrier'):
            barrierCheck = self.__NoMemoryMonthly.copy()
            barrierCheck['couponBarrier'] = 1.2
            StructuredProductFactory.createAutocall(
                **barrierCheck
            )

        with self.assertRaisesRegex(ValueError, 'dates'):
            datesCheck = self.__NoMemoryMonthly.copy()
            datesCheck['startDate'] = date(2023, 9, 1)
            StructuredProductFactory.createAutocall(
                **datesCheck
            )

    def testPaymentDatesMonthly(self):
        self.assertEqual(
            [date(2022, 10, 1), date(2022, 11, 1), date(2022, 12, 1)],
            self.__testedNoMemoryMonthly.getPaymentDates()
        )

    def testPaymentDatesQuarterly(self):
        self.assertEqual(
            [date(2022, 12, 1)],
            self.__testedNoMemoryQuarterly.getPaymentDates()
        )

    def testZeroCouponNoMemory(self):
        sampleMarket = QuoteProviderStub()
        self.assertEqual(
            0,
            self.__testedNoMemoryMonthly.getPaymentAmount(
                date(2022, 10, 1),
                sampleMarket
            ),
        )

    def testNonZeroCouponNoMemory(self):
        sampleMarket = QuoteProviderStub()
        self.assertEqual(
            0.1 / 12,
            self.__testedNoMemoryMonthly.getPaymentAmount(
                date(2022, 11, 1),
                sampleMarket
            ),
        )

    def testNonZeroCouponNoMemory2(self):
        sampleMarket = QuoteProviderStub()
        self.assertEqual(
            (1 + 0.1 / 12),
            self.__testedNoMemoryMonthly.getPaymentAmount(
                date(2022, 12, 1),
                sampleMarket
            ),
        )

    def testNonZeroCouponNoMemoryQuarterly(self):
        sampleMarket = QuoteProviderStub()
        self.assertEqual(
            1.025,
            self.__testedNoMemoryQuarterly.getPaymentAmount(
                date(2022, 12, 1),
                sampleMarket
            ),
        )
