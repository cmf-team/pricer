import plotly.graph_objects
from plotly.subplots import make_subplots
from Markets.MoexQuoteProvider import MoexQuoteProvider
from datetime import date
from typing import List


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
        inspectedObject = MoexQuoteProvider(self.__boardId)
        for i in range(0, len(tickers)):
            chartDf = inspectedObject.getChartQuotes(
                tickers[i],
                startDate,
                endDate
            )
            chart = make_subplots(
                rows=1,
                cols=1,
                vertical_spacing=0.1,
                subplot_titles=(tickers[i], '')
            )
            chart.add_trace(
                plotly.graph_objects.Candlestick(
                    x=chartDf['TRADEDATE'],
                    open=chartDf['OPEN'],
                    high=chartDf['HIGH'],
                    low=chartDf['LOW'],
                    close=chartDf['CLOSE'],
                    name=tickers[i]
                ),
                row=1, col=1
            )
            chart.update(layout_xaxis_rangeslider_visible=False)
            chart.show()


# simple example for plotQuotes method
if __name__ == '__main__':
    tickerList = ['GAZP', 'SBER', 'OZON']
    sampleChartObj = QuoteInspector('TQBR')
    sampleChartObj.plotQuotes(tickerList, date(2022, 1, 1), date(2022, 10, 10))
