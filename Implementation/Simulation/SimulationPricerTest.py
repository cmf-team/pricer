from collections import namedtuple
from datetime import date
from math import exp
from unittest import TestCase
from unittest.mock import Mock

import numpy

from Products.QuoteProvider import QuoteProvider
from Simulation.SimulationPricer import SimulationPricer
from Simulation.CovarianceTermStructure import CovarianceTermStructure
from Simulation.DiscountCurve import DiscountCurve


class SimulationPricerTest(TestCase):
    def setUp(self) -> None:
        mockCovariance = Mock(spec=CovarianceTermStructure)
        mockCovariance.getTotalCovariance = Mock(
            return_value=numpy.array([[0.01]])
        )
        mockQuoteProvider = Mock(spec=QuoteProvider)
        mockQuoteProvider.getQuotes = Mock(
            return_value=[250]
        )

        rate = 0.1
        self.__mockDiscountCurve = Mock(spec=DiscountCurve)
        self.__mockDiscountCurve.getDiscountFactor.return_value = exp(
            -rate * 30 / 365
        )

        self.__testedPricer = SimulationPricer(
            underlyings=["GAZP"],
            underlyingCovarianceForecast=mockCovariance,
            valuationDate=date(2022, 9, 1),
            originalMarket=mockQuoteProvider,
            discountCurve=self.__mockDiscountCurve
        )

    def testDiscountFactor(self):
        sampleDate = date(2022, 9, 1)
        self.assertEqual(
            self.__testedPricer.getDiscountFactor(sampleDate),
            self.__mockDiscountCurve.getDiscountFactor(sampleDate)
        )

    def testCallOptionBasePrice(self):
        testParameters = namedtuple(
            "testParameters",
            ["strike", "expectedResult"]
        )
        testMap = {
            'InTheMoney': testParameters(strike=200, expectedResult=51.715),
            'AtTheMoney': testParameters(strike=250, expectedResult=10.985),
            'OutOfTheMoney': testParameters(strike=300, expectedResult=0.451)
        }
        for testCase, testParams in testMap.items():
            with self.subTest(name=testCase):
                result = self.__testedPricer.getCallOptionBasePrice(
                    underlying="GAZP",
                    strike=testParams.strike,
                    maturityDate=date(2022, 10, 1)
                )

                self.assertEqual(
                    round(result, 3),
                    testParams.expectedResult
                )
