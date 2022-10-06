from datetime import date
from typing import List
from unittest import TestCase

from Products.QuoteProvider import QuoteProvider
from Products.VanillaStructuredProduct import VanillaStructuredProduct


class QuoteProviderStub(QuoteProvider):

    def __init__(self, value: float):
        self.__value = value

    def getQuotes(
        self,
        ticker: str,
        observationDates: List[date]
    ) -> List[float]:

        if ticker == "GAZP" and observationDates == [date(2022, 9, 1)]:
            return [self.__value]
        else:
            raise NotImplementedError()


class VanillaStructuredProductTest(TestCase):

    def setUp(self) -> None:
        self.__testedProduct = VanillaStructuredProduct(
            underlying="GAZP",
            participation=0.65,
            strike=250,
            maturityDate=date(2022, 9, 1)
        )
        self.__testedProductWithCap = VanillaStructuredProduct(
            underlying="GAZP",
            participation=0.65,
            strike=250,
            maturityDate=date(2022, 9, 1),
            cap=0.08,
            profitZoneStart=0.1,
        )

    def testPaymentDates(self):
        self.assertEqual(
            [date(2022, 9, 1)],
            self.__testedProduct.getPaymentDates()
        )

    def testInTheMoneyPayoff(self):
        sampleMarket = QuoteProviderStub(260)
        self.assertEqual(
            1 + 0.65 * 10 / 250,
            self.__testedProduct.getPaymentAmount(
                date(2022, 9, 1),
                sampleMarket
            )
        )

    def testOutOfTheMoneyPayoff(self):
        sampleMarket = QuoteProviderStub(230)
        self.assertEqual(
            1,
            self.__testedProduct.getPaymentAmount(
                date(2022, 9, 1),
                sampleMarket
            )
        )

    def testAtTheMoneyPayoff(self):
        sampleMarket = QuoteProviderStub(250)
        self.assertEqual(
            1,
            self.__testedProduct.getPaymentAmount(
                date(2022, 9, 1),
                sampleMarket
            )
        )

    def testInTheMoneyPayoffWithCapNonCapped(self):
        sampleMarket = QuoteProviderStub(260)
        self.assertEqual(
            1 + 0.65 * 10 / 250,
            self.__testedProductWithCap.getPaymentAmount(
                date(2022, 9, 1),
                sampleMarket
            )
        )

    def testInTheMoneyPayoffWithCapCapped(self):
        sampleMarket = QuoteProviderStub(300)
        self.assertEqual(
            1 + 0.65 * 0.08,
            self.__testedProductWithCap.getPaymentAmount(
                date(2022, 9, 1),
                sampleMarket
            )
        )

    def testOutOfTheMoneyPayoffWithCap(self):
        sampleMarket = QuoteProviderStub(230)
        self.assertEqual(
            1,
            self.__testedProductWithCap.getPaymentAmount(
                date(2022, 9, 1),
                sampleMarket
            )
        )

    def testAtTheMoneyPayoffWithCap(self):
        sampleMarket = QuoteProviderStub(250)
        self.assertEqual(
            1,
            self.__testedProductWithCap.getPaymentAmount(
                date(2022, 9, 1),
                sampleMarket
            )
        )
