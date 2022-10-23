from datetime import date
from unittest import TestCase, main

from Markets.MoexQuoteProvider import MoexQuoteProvider


class MoexQuoteProviderTest(TestCase):
    def setUp(self) -> None:
        self.__testedMoexQuoteProvider = MoexQuoteProvider('TQBR')

    def testReturnedQuotes(self):
        sampleDates = [
            date(2022, 1, 9),
            date(2022, 2, 10),
            date(2022, 10, 3),
            date(2022, 10, 10)
        ]
        self.assertEqual(
            [None, 328.93, 215.83, 163.89],
            self.__testedMoexQuoteProvider.getQuotes('GAZP', sampleDates)
        )
