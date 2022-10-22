from collections import namedtuple
from datetime import date
from typing import List
from unittest import TestCase

from Products.CashFlow import CashFlow
from Products.Pricer import Pricer
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


class PricerStub(Pricer):
    def getValuationDate(self) -> date:
        pass

    def getDiscountFactor(self, paymentDate: date) -> float:
        rate = 0.1
        return -rate * 30 / 365

    def getCashFlowBasePrice(self, pricedElement: CashFlow) -> float:
        pass

    def getCallOptionBasePrice(
        self,
        underlying: str,
        strike: float,
        maturityDate: date
    ) -> float:
        return max(300 - strike, 0)


class VanillaStructuredProductTest(TestCase):
    def setUp(self) -> None:
        self.__maturityDate = date(2022, 9, 1)
        self.__testedUncappedProduct = VanillaStructuredProduct(
            underlying="GAZP",
            participation=0.65,
            strike=250,
            maturityDate=self.__maturityDate
        )
        self.__testedCappedProduct = VanillaStructuredProduct(
            underlying="GAZP",
            participation=0.5,
            strike=250,
            maturityDate=self.__maturityDate,
            cap=0.08
        )
        self.__pricer = PricerStub()

    def testPaymentDates(self):
        self.assertEqual(
            [self.__maturityDate],
            self.__testedUncappedProduct.getPaymentDates()
        )

    def testUncappedPayoff(self):
        testParameters = namedtuple(
            "testParameters",
            ["underlyingQuote", "expectedResult"]
        )
        testMap = {
            'In the money': testParameters(
                underlyingQuote=260,
                expectedResult=1 + 0.65 * 10 / 250
            ),
            'At the money': testParameters(
                underlyingQuote=250,
                expectedResult=1
            ),
            'Out of the money': testParameters(
                underlyingQuote=230,
                expectedResult=1
            )
        }
        for testCase, testParams in testMap.items():
            with self.subTest(testCase):
                self.assertEqual(
                    testParams.expectedResult,
                    self.__testedUncappedProduct.getPaymentAmount(
                        self.__maturityDate,
                        QuoteProviderStub(testParams.underlyingQuote)
                    )
                )

    def testCappedPayoff(self):
        testParameters = namedtuple(
            "testParameters",
            ["underlyingQuote", "expectedResult"]
        )
        testMap = {
            'At the money': testParameters(
                underlyingQuote=250,
                expectedResult=1
            ),
            'Out of the money': testParameters(
                underlyingQuote=230,
                expectedResult=1
            ),
            'In the money, cap strike price': testParameters(
                underlyingQuote=290,
                expectedResult=1 + 0.08
            ),
            'In the money, capped': testParameters(
                underlyingQuote=300,
                expectedResult=1 + 0.08
            ),
            'In the money, non capped': testParameters(
                underlyingQuote=260,
                expectedResult=1 + 0.5 * 10 / 250
            )
        }

        for testCase, testParams in testMap.items():
            with self.subTest(testCase):
                self.assertEqual(
                    testParams.expectedResult,
                    self.__testedCappedProduct.getPaymentAmount(
                        self.__maturityDate,
                        QuoteProviderStub(testParams.underlyingQuote)
                    )
                )

    def testCappedBasePrice(self):
        result = self.__testedCappedProduct.getBasePrice(
            valuationDate=self.__maturityDate,
            pricer=self.__pricer
        )
        callBasePrice = self.__pricer.getCallOptionBasePrice(
            underlying="GAZP",
            strike=250,
            maturityDate=self.__maturityDate
        )
        callCapBasePrice = self.__pricer.getCallOptionBasePrice(
            underlying="GAZP",
            strike=250 * (1 + 0.08 / 0.5),
            maturityDate=self.__maturityDate
        )
        expectedResult = callBasePrice - callCapBasePrice + 1 * \
                         self.__pricer.getDiscountFactor(self.__maturityDate)
        self.assertEqual(expectedResult, result)

    def testUncappedBasePrice(self):
        result = self.__testedUncappedProduct.getBasePrice(
            valuationDate=self.__maturityDate,
            pricer=self.__pricer
        )
        expectedResult = self.__pricer.getCallOptionBasePrice(
            underlying="GAZP",
            strike=250,
            maturityDate=self.__maturityDate
        ) + 1 * self.__pricer.getDiscountFactor(self.__maturityDate)
        self.assertEqual(expectedResult, result)
