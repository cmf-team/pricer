from datetime import date, timedelta

import numpy
from dateutil.rrule import DAILY, rrule

from Products.QuoteProvider import QuoteProvider
from Simulation.CovarianceTermStructure import CovarianceTermStructure


class FlatHistoricalCovarianceForecast(CovarianceTermStructure):
    def __init__(
        self,
        underlyings: list[str],
        observationDate: date,
        historicalWindowSize: int,
        market: QuoteProvider,
        maxNansRate: float = 0.3
    ):
        self.__underlyings = underlyings
        self.__observationDate = observationDate
        self.__market = market
        self.__historicalWindow = [
            historyDate.date() for historyDate in rrule(
                DAILY,
                dtstart=observationDate - timedelta(days=historicalWindowSize),
                until=observationDate
            )
        ][:-1]
        self.__maxNansRate = maxNansRate
        self.__covarianceMatrix = None

    def __checkNansRate(self, quotes) -> None:
        if (
            numpy.isnan(quotes).all(axis=0).sum() >=
            int(self.__maxNansRate * quotes.shape[1])
        ):
            raise ValueError(
                'NaNs rate in historical quotes is higher than '
                'maxNansRate parameter.'
            )

    def __removeNans(self, quotes) -> numpy.ndarray:
        indicesToDelete = numpy.isnan(quotes).any(axis=0)

        self.__historicalWindow = numpy.delete(
            self.__historicalWindow,
            indicesToDelete
        )
        return numpy.delete(quotes, indicesToDelete, axis=1)

    def __getLogChange(self) -> numpy.ndarray:
        quotes = numpy.array(
            [
                self.__market.getQuotes(underlying, self.__historicalWindow)
                for underlying in self.__underlyings
            ]
        )

        self.__checkNansRate(quotes)

        if numpy.isnan(quotes).any():
            quotes = self.__removeNans(quotes)

        return numpy.diff(numpy.log(quotes), axis=1)

    def __initializeCovarianceMatrix(self) -> None:
        logChange = self.__getLogChange()
        historyLength = (
            self.__historicalWindow[-1] - self.__historicalWindow[0]
        ).days
        self.__covarianceMatrix = logChange @ logChange.T / historyLength

    def getObservationDate(self) -> date:
        return self.__observationDate

    def getTotalCovariance(self, forecastDate: date) -> numpy.ndarray:
        if self.__covarianceMatrix is None:
            self.__initializeCovarianceMatrix()

        forecastLength = (forecastDate - self.__observationDate).days
        return self.__covarianceMatrix * forecastLength
