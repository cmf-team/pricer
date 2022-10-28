from datetime import date
from unittest import TestCase

import MoexGCurveQuoteProvider

from Products.QuoteProvider import QuoteProvider

sampleQuoteData = pandas.DataFrame(
    data = {
        date(2022,10,18): 7.6924, 
        date(2022,10,16): 7.6367, #weekend
        date(2022,10,14): 7.6367, 
        date(2022,10,12): 7.7208
    },
    index=[
            'MOEXGCURVE3M'
            ]


class MoexGCurveQuoteProviderTest(TestCase):
    
    def setUp(self) -> None:
        self.__testedQuoteProvider = MoexGCurveQuoteProvider()
    

    def testLastWorkingDayRate(self):
        ticker = 'MOEXGCURVE3M'
        dates = [
            date(2022,10,18), 
            date(2022,10,16), #weekend
            date(2022,10,14),
            date(2022,10,12)
        ]
        
        self.assertEqual(
            sampleQuoteData.loc[ticker, :].values.tolist(),
            self.__testedQuoteProvider.getQuotes(ticker, dates)
        )