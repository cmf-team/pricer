from Products.QuoteProvider import QuoteProvider
from typing import List
import requests
import apimoex
import pandas
import numpy
from datetime import date


class MoexQuoteProvider(QuoteProvider):
    def __init__(
        self,
        boardId: str
    ):
        self.__boardId = boardId

    def getQuotes(
        self,
        ticker: str,
        observationDates: List[date]
    ) -> List[float]:
        startDate: date = min(observationDates)
        endDate: date = max(observationDates)
        columns: tuple = ('TRADEDATE', 'CLOSE')
        pricesList: List[float]
        datesDf = pandas.DataFrame(observationDates)
        datesDf.columns = ['TRADEDATE']
        datesDf['TRADEDATE'] = pandas.to_datetime(
            datesDf['TRADEDATE']
        )

        with requests.Session() as session:
            quotesData = apimoex.get_board_history(
                session,
                ticker,
                startDate,
                endDate,
                columns,
                self.__boardId
            )
            moexDf = pandas.DataFrame(quotesData)
            moexDf['TRADEDATE'] = pandas.to_datetime(moexDf['TRADEDATE'])
            mergedResult = datesDf.merge(
                right=moexDf,
                how='left',
                on='TRADEDATE',
            )
            mergedResult['CLOSE'].replace({numpy.NAN: None}, inplace=True)
            pricesList = mergedResult['CLOSE'].tolist()
        return pricesList

    def getChartQuotes(
        self,
        ticker: str,
        startDate: date,
        endDate: date
    ) -> pandas.DataFrame:
        columns: tuple = (
            'TRADEDATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME')
        with requests.Session() as session:
            chartData = apimoex.get_board_history(
                session,
                ticker,
                startDate,
                endDate,
                columns,
                self.__boardId
            )
            chartDf = pandas.DataFrame(chartData)
        return chartDf
