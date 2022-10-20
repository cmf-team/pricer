import pandas

from datetime import date
from plotly import graph_objects
from typing import List

from Markets.MoexQuoteProvider import MoexQuoteProvider
from Products.QuoteProvider import QuoteProvider

class QuoteInspector:
    def __init__(self, inspectedObject: QuoteProvider):
        self.__inspectedObject = inspectedObject
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
        for ticker in tickers:
            observationPrices = self.__inspectedObject.getQuotes(
                ticker,
                observationDates
            )
            chartDf = pandas.DataFrame(
                list(zip(observationDates, observationPrices)),
                columns=['TRADEDATE', 'CLOSE']
            )
            chartDf.dropna(subset=['CLOSE'], inplace=True)
            chart = graph_objects.Figure(
                data=graph_objects.Scatter(
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
    sampleQuoteObject= MoexQuoteProvider('TQBR')
    sampleChartObject = QuoteInspector(sampleQuoteObject)
    sampleChartObject.plotQuotes(
        tickerList,
        date(2022, 1, 1),
        date(2022, 10, 10)
    )
