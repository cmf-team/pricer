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
        self.__testedUncappedProduct = VanillaStructuredProduct(
            underlying="GAZP",
            participation=0.65,
            strike=250,
            maturityDate=date(2022, 9, 1),
        )
        self.__testedСappedProduct = VanillaStructuredProduct(
            underlying="GAZP",
            participation=0.5,
            strike=250,
            maturityDate=date(2022, 9, 1),
            cap=0.08,
        )

    def testPaymentDates(self):
        self.assertEqual(
            [date(2022, 9, 1)],
            self.__testedUncappedProduct.getPaymentDates()
        )

    def testInTheMoneyPayoff(self):
        sampleMarket = QuoteProviderStub(260)
        self.assertEqual(
            1 + 0.65 * 10 / 250,
            self.__testedUncappedProduct.getPaymentAmount(
                date(2022, 9, 1),
                sampleMarket
            ),
        )

    def testOutOfTheMoneyPayoff(self):
        sampleMarket = QuoteProviderStub(230)
        self.assertEqual(
            1,
            self.__testedUncappedProduct.getPaymentAmount(
                date(2022, 9, 1),
                sampleMarket
            ),
        )

    def testAtTheMoneyPayoff(self):
        sampleMarket = QuoteProviderStub(250)
        self.assertEqual(
            1,
            self.__testedUncappedProduct.getPaymentAmount(
                date(2022, 9, 1),
                sampleMarket
            ),
        )

    def testInTheMoneyPayoffWithCapNonCapped(self):
        sampleMarket = QuoteProviderStub(260)
        self.assertEqual(
            1 + 0.5 * 10 / 250,
            self.__testedСappedProduct.getPaymentAmount(
                date(2022, 9, 1),
                sampleMarket
            ),
        )

    def testInTheMoneyPayoffWithCapCapped(self):
        sampleMarket = QuoteProviderStub(300)
        self.assertEqual(
            1 + 0.5 * 0.08,
            self.__testedСappedProduct.getPaymentAmount(
                date(2022, 9, 1),
                sampleMarket
            ),
        )

    def testInTheMoneyPayoffWithCapCappedStrikePrice(self):
        sampleMarket = QuoteProviderStub(290)
        self.assertEqual(
            1 + 0.5 * 0.08,
            self.__testedСappedProduct.getPaymentAmount(
                date(2022, 9, 1),
                sampleMarket
            ),
        )

    def testOutOfTheMoneyPayoffWithCap(self):
        sampleMarket = QuoteProviderStub(230)
        self.assertEqual(
            1,
            self.__testedСappedProduct.getPaymentAmount(
                date(2022, 9, 1),
                sampleMarket
            ),
        )

    def testAtTheMoneyPayoffWithCap(self):
        sampleMarket = QuoteProviderStub(250)
        self.assertEqual(
            1,
            self.__testedСappedProduct.getPaymentAmount(
                date(2022, 9, 1),
                sampleMarket
            ),
        )
