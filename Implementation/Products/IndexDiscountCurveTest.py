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

    def testOneTenor(self):
        self.__testedCurve = IndexDiscountCurve(
            valuationDate=date(2022, 9, 1),
            tenors=['1W'],
            tickers=["GAZP_1W"],
            market=QuoteProviderDisc({'GAZP_1W': 7.5}),
        )
        self.assertEqual(0.9992, round(self.__testedCurve.getDiscountFactor(date(2022, 9, 5)), 4))

    def testTwoTenors(self):
        self.__testedCurve = IndexDiscountCurve(
            valuationDate=date(2022, 9, 1),
            tenors=['1D', '1W'],
            tickers=["GAZP_1D", "GAZP_1W"],
            market=QuoteProviderDisc({'GAZP_1D': 5.0, 'GAZP_1W': 10}),
        )
        self.assertEqual(0.9992, round(self.__testedCurve.getDiscountFactor(date(2022, 9, 5)), 4))
    
    def testExtrapolation(self):
        self.__testedCurve = IndexDiscountCurve(
            valuationDate=date(2022, 9, 1),
            tenors=['1D', '1W'],
            tickers=["GAZP_1D", "GAZP_1W"],
            market=QuoteProviderDisc({'GAZP_1D': 5.0, 'GAZP_1W': 10}),
        )
        self.assertEqual(0.9702, round(self.__testedCurve.getDiscountFactor(date(2022, 10, 5)), 4))
