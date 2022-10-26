from unittest import TestCase
from datetime import date
from typing import List, Dict, Optional
from Products.IndexDiscountCurve import IndexDiscountCurve
from Products.QuoteProvider import QuoteProvider


class QuoteProviderStub(QuoteProvider):
    def __init__(self, tickerValues: Dict):
        self.__tickerValues = tickerValues

    def getQuotes(
        self,
        ticker: str,
        observationDates: List[date]
    ) -> Optional[List[float]]:

        if observationDates == [date(2022, 9, 1)]:
            for key in self.__tickerValues.keys():
                if ticker == key:
                    return [self.__tickerValues[key]]
        else:
            raise NotImplementedError()

        return [None]


class VanillaStructuredProductTest(TestCase):
    def setUp(self):
        self.__testedCurve = IndexDiscountCurve(
            valuationDate=date(2022, 9, 1),
            tenors=['1D', '1W', '1M', '1Y'],
            tickers=["RATE1D", "RATE1W", "RATE1M", "RATE1Y"],
            market=QuoteProviderStub({
                'RATE1D': 0.5,
                'RATE1W': 1.3,
                'RATE1M': 3.6,
                'RATE1Y': 12.9,
            }),
        )

        self.__testedCurveOneTenor = IndexDiscountCurve(
            valuationDate=date(2022, 9, 1),
            tenors=['1D'],
            tickers=["RATE1D"],
            market=QuoteProviderStub({
                'RATE1D': 0.5,
            }),
        )
    
    def testCurveOneTenor(self):
        self.assertEqual(0.999945, round(
            self.__testedCurveOneTenor.getDiscountFactor(date(2022, 9, 5)), 6)
        )

    def testDayInterpolation(self):
        self.assertEqual(0.999901, round(
            self.__testedCurve.getDiscountFactor(date(2022, 9, 5)), 6)
        )

    def testDayPointValue(self):
        self.assertEqual(1, round(
            self.__testedCurve.getDiscountFactor(date(2022, 9, 1)), 6)
        )

    def testWeekInterpolation(self):
        self.assertEqual(0.99963, round(
            self.__testedCurve.getDiscountFactor(date(2022, 9, 10)), 6)
        )

    def testWeekPointValue(self):
        self.assertEqual(0.999751, round(
            self.__testedCurve.getDiscountFactor(date(2022, 9, 8)), 6)
        )

    def testMonthInterpolation(self):
        self.assertEqual(0.995895, round(
            self.__testedCurve.getDiscountFactor(date(2022, 10, 10)), 6)
        )

    def testMonthPointValue(self):
        self.assertEqual(0.997045, round(
            self.__testedCurve.getDiscountFactor(date(2022, 10, 1)), 6)
        )

    def testYearInterpolation(self):
        self.assertEqual(0.977278, round(
                self.__testedCurve.getDiscountFactor(date(2023, 1, 10)), 6)
        )

    def testYearPointValue(self):
        self.assertEqual(0.878974, round(
            self.__testedCurve.getDiscountFactor(date(2023, 9, 1)), 6)
        )

    def testExtrapolation(self):
        self.assertEqual(0.176535, round(
            self.__testedCurve.getDiscountFactor(date(2026, 9, 1)), 6)
        )
