from datetime import date
from unittest import TestCase
from unittest.mock import patch

from Markets.MoexQuoteProvider import MoexQuoteProvider


# Quotes expected to be returned by apimoex.get_board_history for GAZP ticker
sampleQuoteData = [
    {'TRADEDATE': '2022-01-07', 'CLOSE': None},
    {'TRADEDATE': '2022-02-10', 'CLOSE': 328.93},
    {'TRADEDATE': '2022-10-03', 'CLOSE': 215.83},
    {'TRADEDATE': '2022-10-10', 'CLOSE': 163.89}
]


class MoexQuoteProviderTest(TestCase):

    def setUp(self) -> None:
        self.__testedQuoteProvider = MoexQuoteProvider("TQBR")

    @patch('apimoex.get_board_history')
    def testQuotes(self, mock_get_board_history):
        sampleDates = [
            date(2022, 1, 7),
            date(2022, 1, 10),
            date(2022, 2, 10),
            date(2022, 10, 3),
            date(2022, 10, 10)
        ]
        mock_get_board_history.return_value = sampleQuoteData
        self.assertEqual(
            [None, None, 328.93, 215.83, 163.89],
            self.__testedQuoteProvider.getQuotes('GAZP', sampleDates)
        )
        mock_get_board_history.assert_called()
