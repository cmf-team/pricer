from unittest import TestCase
from datetime import date
from typing import List
from Products.IndexDiscountCurve import IndexDiscountCurve
from Products.QuoteProvider import QuoteProvider


class QuoteProviderDisc(QuoteProvider):
    def __init__(self, ticker_values: map):
        self.__tickerValues = ticker_values

    def getQuotes(
        self,
        ticker: str,
        observationDates: List[date]
    ) -> List[float]:

        if observationDates == [date(2022, 9, 1)]:
            for key in self.__tickerValues.keys():
                if ticker == key:
                    return [self.__tickerValues[key]]
        else:
            raise NotImplementedError()


class VanillaStructuredProductTest(TestCase):
    def setUp(self):
        self.__testedCurve = IndexDiscountCurve(
            valuationDate=date(2022, 9, 1),
            tenors=['1D', '1W', '1M', '1Y'],
            tickers=["RATE1D", "RATE1W", "RATE1M", "RATE1Y"],
            market=QuoteProviderDisc({'RATE1D': 0.5, 'RATE1W': 1.3, 'RATE1M': 3.6, 'RATE1Y': 12.9}),
        )

    def testDayInterpolation(self):
        self.assertEqual(0.9999, round(
            self.__testedCurve.getDiscountFactor(date(2022, 9, 5)), 4)
        )

    def testDayPointValue(self):
        self.assertEqual(1, round(
            self.__testedCurve.getDiscountFactor(date(2022, 9, 1)), 4)
        )

    def testWeekInterpolation(self):
        self.assertEqual(0.9996, round(
            self.__testedCurve.getDiscountFactor(date(2022, 9, 10)), 4)
        )

    def testWeekPointValue(self):
        self.assertEqual(0.9998, round(
            self.__testedCurve.getDiscountFactor(date(2022, 9, 8)), 4)
        )

    def testMonthInterpolation(self):
        self.assertEqual(0.9959, round(
            self.__testedCurve.getDiscountFactor(date(2022, 10, 10)), 4)
        )

    def testMonthPointValue(self):
        self.assertEqual(0.997, round(
            self.__testedCurve.getDiscountFactor(date(2022, 10, 1)), 4)
        )

    def testYearInterpolation(self):
        self.assertEqual(0.9773, round(
                self.__testedCurve.getDiscountFactor(date(2023, 1, 10)), 4)
        )

    def testYearPointValue(self):
        self.assertEqual(0.8619, round(
            self.__testedCurve.getDiscountFactor(date(2023, 10, 1)), 4)
        )
    
    def testExtrapolation(self):
        self.assertEqual(0.1765, round(
            self.__testedCurve.getDiscountFactor(date(2026, 9, 1)), 4)
        )
