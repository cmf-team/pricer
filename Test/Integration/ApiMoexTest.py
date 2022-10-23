import os
import sys
from unittest import TestCase

import apimoex
import requests

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "Implementation"
    )
)
from Markets.MoexQuoteProviderTest import sampleQuoteData


class ApiMoexTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.__session = requests.Session()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.__session.close()

    def testStockQuotesFeed(self):
        for expectedQuote in sampleQuoteData:
            with self.subTest(f"GAZP @ {expectedQuote['TRADEDATE']}"):
                pass
                self.assertIn(
                    expectedQuote,
                    apimoex.get_board_history(
                        self.__session,
                        'GAZP',
                        '2022-01-07',
                        '2022-10-10',
                        ('TRADEDATE', 'CLOSE'),
                        'TQBR'
                    )
                )
