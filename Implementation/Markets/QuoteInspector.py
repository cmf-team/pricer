import plotly.graph_objects
from Markets.MoexQuoteProvider import MoexQuoteProvider
from datetime import date
from typing import List
import pandas


class QuoteInspector:
    def __init__(
        self,
        boardId: str
    ):
        self.__boardId = boardId

    def plotQuotes(
        self,
        tickers: List[str],
        startDate: date,
        endDate: date,
    ) -> None:
        observationDates = pandas.date_range(
            start=startDate,
            end=endDate
        ).tolist()
        inspectedObject = MoexQuoteProvider(self.__boardId)
        for ticker in tickers:
            observationPrices = inspectedObject.getQuotes(
                ticker,
                observationDates
            )
            chartDf = pandas.DataFrame(
                list(zip(observationDates, observationPrices)),
                columns=['TRADEDATE', 'CLOSE']
            )
            chartDf.dropna(subset=['CLOSE'], inplace=True)
            chart = plotly.graph_objects.Figure(
                data=plotly.graph_objects.Scatter(
                    x=chartDf['TRADEDATE'],
                    y=chartDf['CLOSE'],
                    mode='lines',
                )
            )
            chart.update_layout(title=ticker)
            chart.show()


# simple example for plotQuotes method
if __name__ == '__main__':
    tickerList = ['GAZP', 'SBER', 'OZON']
    sampleChartObject = QuoteInspector('TQBR')
    sampleChartObject.plotQuotes(
        tickerList,
        date(2022, 1, 1),
        date(2022, 10, 10)
    )
