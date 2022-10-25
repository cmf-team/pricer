from unittest import TestCase

import apimoex
import requests

from Markets.MoexQuoteProviderTest import sampleQuoteData


class ApiMoexTest(TestCase):

    def testStockQuotesFeed(self):
        with requests.Session() as session:
            serviceQuotes = apimoex.get_board_history(
                session,
                'GAZP',
                '2022-01-07',
                '2022-10-10',
                ('TRADEDATE', 'CLOSE'),
                'TQBR'
            )
            for expectedQuote in sampleQuoteData:
                with self.subTest(f"GAZP @ {expectedQuote['TRADEDATE']}"):
                    self.assertIn(expectedQuote, serviceQuotes)
