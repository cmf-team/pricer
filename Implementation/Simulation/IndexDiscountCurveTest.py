from datetime import date
from typing import Dict, List
from unittest import TestCase

from Products.QuoteProvider import QuoteProvider

from Simulation.IndexDiscountCurve import IndexDiscountCurve


class QuoteProviderStub(QuoteProvider):
    def __init__(self, quoteData: Dict[str, float]):
        """Class that provides rates and quotes for certain observation date.
        Args:
            quoteData (Dict[str, float]): Dict with quotes and their rates.
            Where key is tha name of a quote and rate is the precentage
            rate in percents.
        """
        acceptableDurations = ['D', 'W', 'M', 'Y']
        for quote in quoteData.items():
            durationType = quote[0][-1]
            if durationType not in acceptableDurations:
                raise ValueError('Ticker should end with D, W, M or Y')
        self.__tickerValues = quoteData

    def getTickerValues(self):
        return self.__tickerValues

    def getQuotes(
        self,
        ticker: str,
        observationDates: List[date]
    ) -> List[float]:

        if observationDates == [date(2022, 9, 1)]:
            if ticker in self.__tickerValues.keys():
                return [self.__tickerValues[ticker]]
            raise ValueError('No rate for such ticker')
        else:
            raise NotImplementedError()


class VanillaStructuredProductTest(TestCase):
    def setUp(self):
        self.__testedCurve = IndexDiscountCurve(
            valuationDate=date(2022, 9, 1),
            tenors=['1D', '1Y', '1M', '1W'],
            tickers=['RATE1D', 'RATE1Y', 'RATE1M', 'RATE1W'],
            market=QuoteProviderStub({
                'RATE1D': 0.5,
                'RATE1W': 1.3,
                'RATE1M': 1.2,
                'RATE1Y': 12.9,
            }),
        )

        self.__testedCurveOneTenor = IndexDiscountCurve(
            valuationDate=date(2022, 9, 1),
            tenors=['1D'],
            tickers=["RATE1D"],
            market=QuoteProviderStub({'RATE1D': 0.5}),
        )

    def testSwapQuotes(self):
        marketOne = QuoteProviderStub({
            'RATE1D': 0.5,
            'RATE1W': 1.3,
            'RATE1M': 1.2,
            'RATE1Y': 12.9,
        })
        marketTwo = QuoteProviderStub({
            'RATE1W': 1.3,
            'RATE1M': 1.2,
            'RATE1Y': 12.9,
            'RATE1D': 0.5,
        })

        self.assertEqual(
            marketOne.getTickerValues(),
            marketTwo.getTickerValues()
        )

    def testCurveOneTenor(self):
        self.assertAlmostEqual(
            0.999945,
            self.__testedCurveOneTenor.getDiscountFactor(date(2022, 9, 5)),
            6,
        )

    def testDayInterpolation(self):
        self.assertAlmostEqual(
            0.999901,
            self.__testedCurve.getDiscountFactor(date(2022, 9, 5)),
            6,
        )

    def testZeroPointValue(self):
        self.assertAlmostEqual(
            1,
            self.__testedCurve.getDiscountFactor(date(2022, 9, 1)),
            6
        )

    def testWeekInterpolation(self):
        self.assertAlmostEqual(
            0.999682,
            self.__testedCurve.getDiscountFactor(date(2022, 9, 10)),
            6,
        )

    def testWeekPointValue(self):
        self.assertAlmostEqual(
            0.999751,
            self.__testedCurve.getDiscountFactor(date(2022, 9, 8)),
            6,
        )

    def testMonthInterpolation(self):
        self.assertAlmostEqual(
            0.998383,
            self.__testedCurve.getDiscountFactor(date(2022, 10, 10)),
            6,
        )

    def testMonthPointValue(self):
        self.assertAlmostEqual(
            0.999014,
            self.__testedCurve.getDiscountFactor(date(2022, 10, 1)),
            6,
        )

    def testYearInterpolation(self):
        self.assertAlmostEqual(
            0.983176,
            self.__testedCurve.getDiscountFactor(date(2023, 1, 10)),
            6,
        )

    def testYearPointValue(self):
        self.assertAlmostEqual(
            0.878974,
            self.__testedCurve.getDiscountFactor(date(2023, 9, 1)),
            6,
        )

    def testExtrapolation(self):
        self.assertAlmostEqual(
            0.5966924,
            self.__testedCurve.getDiscountFactor(date(2026, 9, 1)),
            6,
        )

    def testSameRates(self):

        self.assertRaises(
            ValueError,
            IndexDiscountCurve,
            valuationDate=date(2022, 9, 1),
            tenors=['1D', '1D'],
            tickers=["RATE1D", "RATE1D"],
            market=QuoteProviderStub({'RATE1D': 1.5}),
        )

    def testQuoteName(self):
        self.assertRaises(
            ValueError,
            QuoteProviderStub,
            quoteData={'RATE1B': 1.5},
        )

    def testTenor(self):
        self.assertRaises(
            ValueError,
            IndexDiscountCurve,
            valuationDate=date(2022, 9, 1),
            tenors=['1B'],
            tickers=["RATE1B"],
            market=QuoteProviderStub({'RATE1D': 1.5}),
        )

    def testMismatch(self):
        self.assertRaises(
            ValueError,
            IndexDiscountCurve,
            valuationDate=date(2022, 9, 1),
            tenors=['1D'],
            tickers=["RATE2D"],
            market=QuoteProviderStub({'RATE1D': 1.5}),
        )
