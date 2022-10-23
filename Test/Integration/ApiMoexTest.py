import os
import sys
from unittest import TestCase

import apimoex
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from Implementation.Markets.MoexQuoteProviderTest import sampleQuoteData


class ApiMoexTest(TestCase):

    def testStockQuotesFeed(self):
        with requests.Session() as session:
            for expectedQuote in sampleQuoteData:
                with self.subTest(f"GAZP @ {expectedQuote['TRADEDATE']}"):
                    self.assertIn(
                        expectedQuote,
                        apimoex.get_board_history(
                            session,
                            'GAZP',
                            '2022-01-07',
                            '2022-10-10',
                            ('TRADEDATE', 'CLOSE'),
                            'TQBR'
                        )
                    )
