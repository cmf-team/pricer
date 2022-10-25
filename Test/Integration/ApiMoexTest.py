import os
import sys
from unittest import TestCase
from unittest.mock import Mock, patch

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

    __session = requests.Session()

    # @classmethod
    # def setUpClass(cls) -> None:
    #     cls.__session = requests.Session()

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     pass
    #     # cls.__session.close()

    @patch.object(__session, __session.get.__name__)
    def testStockQuotesFeed(self, mockMethod):
        mockSession = Mock(spec=requests.Session)
        # mockSession.get = Mock(return_value = session.get(
        #     url='https://iss.moex.com/iss/history/engines/stock/markets'
        #         '/shares/boards/TQBR/securities/GAZP.json',
        #     params={
        #         'from': '2022-10-09',
        #         'to': '2022-10-10',
        #         'iss.only': 'history,history.cursor',
        #         'history.columns': 'TRADEDATE,CLOSE'
        #     }
        # )
        # )
        # print(
        #     session.get(url="https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/GAZP.json?iss.json=extended&iss.meta=off&from=2022-10-09&till=2022-10-10&iss.only=history%2Chistory.cursor&history.columns=TRADEDATE%2CCLOSE").content
        # )

        # mockSession.get = lambda url, **kwargs: (session.get(url, **kwargs), print(session.request(method='get', url=url, params=kwargs['params'])))[0]

        def getData(url, **kwargs):
            session = requests.Session()
            result = session.get(
                url="https://iss.moex.com/iss/history/engines/stock/markets"
                    "/shares/boards/TQBR/securities/GAZP.json?iss.json"
                    "=extended&iss.meta=off&from=2022-01-07&till=2022-10-10"
                    "&iss.only=history%2Chistory.cursor&history.columns=TRADEDATE%2CCLOSE"
            )
            session.close()
            return result

        mockSession.get = getData
            # lambda url, **kwargs: \
            # session.get(url="https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/GAZP.json?iss.json=extended&iss.meta=off&from=2022-01-07&till=2022-10-10&iss.only=history%2Chistory.cursor&history.columns=TRADEDATE%2CCLOSE")

        # print(mockSession.get(1, x=1).content)
        # print(
        #     apimoex.get_board_history(
        #         mockSession,
        #         'GAZP'
        #     )
        # )
        with requests.Session() as session:
            serviceData = apimoex.get_board_history(
                session,
                'GAZP',
                '2022-01-07',
                '2022-10-10',
                ('TRADEDATE', 'CLOSE'),
                'TQBR'
            )
        for expectedQuote in sampleQuoteData:
            with self.subTest(f"GAZP @ {expectedQuote['TRADEDATE']}"):
                self.assertIn(expectedQuote, serviceData)
