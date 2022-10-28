from datetime import date
from unittest import TestCase

from Simulation.FlatHistoricalCovarianceForecast import \
    FlatHistoricalCovarianceForecast
from Products.QuoteProvider import QuoteProvider

GAZPQuotes = {
    date(2022, 9, 1): 100,
    date(2022, 9, 2): 105,
    date(2022, 9, 3): 101,
    date(2022, 9, 4): 106,
}

YNDXQuotes = {
    date(2022, 9, 1): 150,
    date(2022, 9, 2): 130,
    date(2022, 9, 3): 155,
    date(2022, 9, 4): 155,
}


class QuoteProviderStub(QuoteProvider):
    def __init__(self):
        pass

    def getQuotes(
        self,
        ticker: str,
        observationDates: list[date]
    ) -> list[float]:

        if ticker == "GAZP":
            try:
                return [
                    GAZPQuotes.get(observationDate) for
                    observationDate in observationDates
                ]
            except KeyError:
                raise NotImplementedError()

        if ticker == "YNDX":
            try:
                return [
                    YNDXQuotes.get(observationDate) for
                    observationDate in observationDates
                ]
            except KeyError:
                raise NotImplementedError()


class AutocallTest(TestCase):
    def setUp(self) -> None:
        sampleMarket = QuoteProviderStub()
        self.__tested = FlatHistoricalCovarianceForecast(
            underlyings=['GAZP', 'YNDX'],
            observationDate=date(2022, 9, 5),
            historicalWindowSize=4,
            market=sampleMarket,
            maxNansRate=0.3
        )

    def testGetObservationDate(self):
        self.assertEqual(
            date(2022, 9, 5),
            self.__tested.getObservationDate()
        )
