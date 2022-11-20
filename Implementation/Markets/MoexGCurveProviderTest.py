from datetime import date, timedelta
from unittest import TestCase

from Markets.MoexGCurveQuoteProvider import MoexGCurveQuoteProvider


class MoexGCurveProviderTest(TestCase):

    def setUp(self) -> None:
        self.__testedQuoteProvider = MoexGCurveQuoteProvider()

    def testProvidedQuotes(self):
        sampleDates = [
            date(2022,10,18),
            date(2022, 10, 16), #weekend
            date(2022, 10, 14),
            date(2022, 10, 12),
            date.today() + timedelta(days=1) #future date
        ]

        self.assertEqual(
            [7.6924, None, 7.6367, 7.7208, None],
            self.__testedQuoteProvider.getQuotes('MOEXGCURVE3M', sampleDates)
        )