from datetime import date
from typing import List

import apimoex
import numpy
import pandas
import requests

from Products.QuoteProvider import QuoteProvider


class MoexQuoteProvider(QuoteProvider):
    def __init__(self, boardId: str):
        self.__boardId = boardId

    def getQuotes(
        self,
        ticker: str,
        observationDates: List[date]
    ) -> List[float]:
        startDate = min(observationDates)
        endDate = max(observationDates)
        resultDates = pandas.DataFrame(observationDates)
        resultDates.columns = ['TRADEDATE']
        resultDates['TRADEDATE'] = pandas.to_datetime(
            resultDates['TRADEDATE']
        )

        with requests.Session() as session:
            quoteData = pandas.DataFrame(
                apimoex.get_board_history(
                    session,
                    ticker,
                    startDate.strftime("%Y-%m-%d"),
                    endDate.strftime("%Y-%m-%d"),
                    ('TRADEDATE', 'CLOSE'),
                    self.__boardId
                )
            )
            quoteData = pandas.DataFrame(quoteData)
            quoteData['TRADEDATE'] = pandas.to_datetime(quoteData['TRADEDATE'])
            result = resultDates.merge(
                right=quoteData,
                how='left',
                on='TRADEDATE',
            )
            result['CLOSE'].replace({numpy.NAN: None}, inplace=True)
        return result['CLOSE'].tolist()
