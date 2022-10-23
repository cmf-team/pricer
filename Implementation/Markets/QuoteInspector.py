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
        observationDates = self.__getHistoricalWindow(startDate, endDate)
        for ticker in tickers:
            observationPrices = self.__inspectedObject.getQuotes(
                ticker,
                observationDates
            )
            plottedData = pandas.DataFrame(
                list(zip(observationDates, observationPrices)),
                columns=['TRADEDATE', 'CLOSE']
            )
            plottedData.dropna(subset=['CLOSE'], inplace=True)
            chart = graph_objects.Figure(
                data=graph_objects.Scatter(
                    x=plottedData['TRADEDATE'],
                    y=plottedData['CLOSE'],
                    mode='lines+markers',
                )
            )
            chart.update_layout(title=ticker)
            chart.show()

    @staticmethod
    def __getHistoricalWindow(startDate: date, endDate: date) -> List[date]:
        return pandas.date_range(start=startDate, end=endDate).tolist()


# simple example for plotQuotes method
if __name__ == '__main__':
    sampleTickers = ['GAZP', 'SBER', 'OZON']
    sampleQuoteObject = MoexQuoteProvider('TQBR')
    sampleChartObject = QuoteInspector(sampleQuoteObject)
    sampleChartObject.plotQuotes(
        sampleTickers,
        date(2022, 1, 1),
        date(2022, 10, 10)
    )
