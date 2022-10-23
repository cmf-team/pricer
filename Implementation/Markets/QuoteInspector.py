import os.path
from datetime import date, timedelta
from typing import List

import pandas
from plotly import graph_objects

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

    def exportQuotes(
        self,
        tickers: List[str],
        startDate: date,
        endDate: date,
        outputFilePath: str
    ):
        """
        Exports quotes for given tickers and observation period to Excel file.

        :param outputFilePath: Path to Excel file in existing directory to
            export quotes to.
        """
        if not os.path.exists(os.path.dirname(outputFilePath)):
            raise ValueError(
                f"Directory {os.path.dirname(outputFilePath)} does not exist."
            )
        if not outputFilePath.endswith(".xlsx"):
            raise ValueError(
                f"Wrong file extension {outputFilePath.split('.')[-1]}."
            )
        observationDates = self.__getHistoricalWindow(startDate, endDate)
        output = pandas.DataFrame()
        output["Date"] = observationDates
        for ticker in tickers:
            output[ticker] = self.__inspectedObject.getQuotes(
                ticker,
                observationDates
            )
        output = output.set_index("Date")
        output.to_excel(outputFilePath, index_label="Date")

    @staticmethod
    def __getHistoricalWindow(startDate: date, endDate: date) -> List[date]:
        return [
            startDate + timedelta(days=dateIndex)
            for dateIndex in range((endDate - startDate).days + 1)
        ]


# Example of QuoteInspector use
if __name__ == '__main__':
    sampleTickers = ['GAZP', 'SBER', 'OZON']
    sampleStartDate = date(2022, 1, 1)
    sampleEndDate = date(2022, 10, 10)
    sampleQuoteObject = MoexQuoteProvider('TQBR')
    sampleQuoteInspector = QuoteInspector(sampleQuoteObject)
    sampleQuoteInspector.plotQuotes(
        tickers=sampleTickers,
        startDate=sampleStartDate,
        endDate=sampleEndDate
    )
    sampleQuoteInspector.exportQuotes(
        tickers=sampleTickers,
        startDate=sampleStartDate,
        endDate=sampleEndDate,
        outputFilePath=os.path.join(
            os.path.dirname(__file__),
            "QuoteData.xlsx"
        )
    )
