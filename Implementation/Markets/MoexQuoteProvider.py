# getting quotes with apimoex library
# apimoex should be installed — https://pypi.org/project/apimoex/
# installation through terminal — pip install apimoex

from Products.QuoteProvider import QuoteProvider
from typing import List
import requests
import apimoex
import pandas as pd
from datetime import date
import plotly.graph_objects as go
from plotly.subplots import make_subplots



class MoexQuoteProvider(QuoteProvider):
    def __init__(
        self,
        boardId: str
    ): self.__boardId = boardId

    def getQuotes(
        self,
        ticker: str,
        observationDates: List[date]
    ) -> List[float]:
        self.__ticker = ticker
        self.__startDate: date = min(observationDates)
        self.__endDate: date = max(observationDates)
        self.__columns: tuple = ('TRADEDATE', 'CLOSE')
        self.__pricesList: List[float]
        self.__observationDates = pd.DataFrame(observationDates)
        self.__observationDates.columns = ['TRADEDATE']
        self.__observationDates['TRADEDATE'] = pd.to_datetime(
        self.__observationDates['TRADEDATE']
        )

        with requests.Session() as session:
            self.__quotesData = apimoex.get_board_history(
                session,
                self.__ticker,
                self.__startDate,
                self.__endDate,
                self.__columns,
                self.__boardId
            )
            self.__moexDf = pd.DataFrame(self.__quotesData)
            self.__moexDf['TRADEDATE'] = pd.to_datetime(
                self.__moexDf['TRADEDATE']
            )
            self.__mergedResult = self.__observationDates.merge(
                right=self.__moexDf,
                how='left',
                on='TRADEDATE'
            )
            self.__pricesList = self.__mergedResult['CLOSE'].tolist()
        return self.__pricesList

    def getChart(
        self,
        ticker: str,
        startDate: date,
        endDate: date
    ):
        self.__ticker = ticker
        self.__startDate = startDate
        self.__endDate = endDate
        self.__columns: tuple = (
        'TRADEDATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME')
        with requests.Session() as session:
            self.__chartData = apimoex.get_board_history(
                session,
                self.__ticker,
                self.__startDate,
                self.__endDate,
                self.__columns,
                self.__boardId
            )
            self.__chartDf = pd.DataFrame(self.__chartData)
            self.__chart = make_subplots(
                rows=2,
                cols=1,
                shared_xaxes=True,
                vertical_spacing=0.1,
                subplot_titles=(self.__ticker, 'Volume'),
                row_width=[0.2, 0.7]
            )
            self.__chart.add_trace(
                go.Candlestick(
                    x=self.__chartDf['TRADEDATE'],
                    open=self.__chartDf['OPEN'],
                    high=self.__chartDf['HIGH'],
                    low=self.__chartDf['LOW'],
                    close=self.__chartDf['CLOSE'],
                    name=self.__ticker
                ),
                row=1, col=1
            )
            self.__chart.add_trace(
                go.Bar(
                    x=self.__chartDf['TRADEDATE'],
                    y=self.__chartDf['VOLUME'],
                    showlegend=False
                ),
                row=2, col=1
            )
            self.__chart.update(layout_xaxis_rangeslider_visible=False)
            self.__chart.show()
        pass



# simple test for getQuotes method
sampleQuoteObj = MoexQuoteProvider('TQBR')
sampleDates = [date(2022, 1, 9), date(2022, 2, 10), date(2022, 10, 3),
    date(2022, 10, 10)]

samplePrices = sampleQuoteObj.getQuotes('GAZP', sampleDates)
for i in range(0, len(sampleDates)):
    print(sampleDates[i], samplePrices[i])

# simple test for getChart method
sampleChartObj=MoexQuoteProvider('TQBR')
sampleQuoteObj.getChart('GAZP',date(2022,1,1),date(2022,10,10))
sampleQuoteObj.getChart('SBER',date(2022,1,1),date(2022,10,10))