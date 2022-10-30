from datetime import date

import numpy
from dateutil.rrule import DAILY, rrule
from pandas.tseries.offsets import BusinessDay

from Products.QuoteProvider import QuoteProvider
from Simulation.CovarianceTermStructure import CovarianceTermStructure


class FlatSampleCovarianceForecast(CovarianceTermStructure):
    """
    missedQuotesLimit: The maximum percentage of missed quotes. If there are
    \n more missing quotes that this rate, the function throws an exception.
    """

    def __init__(
        self,
        underlyings: list[str],
        observationDate: date,
        samplelWindowSize: int,
        market: QuoteProvider,
        missedQuotesLimit: float = 0.3
    ):
        self.__underlyings = underlyings
        self.__observationDate = observationDate
        self.__market = market
        self.__sampleWindow = [
            sampleDate.date() for sampleDate in rrule(
                DAILY,
                dtstart=observationDate - BusinessDay(samplelWindowSize),
                until=observationDate,
                byweekday=(0, 1, 2, 3, 4)
            )
        ][1:]
        self.__missedQuotesLimit = missedQuotesLimit
        self.__covarianceMatrix = None

    def __checkNansRate(self, quotes) -> None:
        if (
            numpy.isnan(quotes).all(axis=0).sum() >=
            int(self.__missedQuotesLimit * quotes.shape[1])
        ):
            raise ValueError(
                'The percentage of missed quotes is higher than '
                'missedQuotesLimit parameter.'
            )

    def __removeNans(self, quotes) -> numpy.ndarray:
        indicesToDelete = numpy.isnan(quotes).any(axis=0)

        self.__sampleWindow = numpy.delete(
            self.__sampleWindow,
            indicesToDelete
        )
        return numpy.delete(quotes, indicesToDelete, axis=1)

    def __getLogChange(self) -> numpy.ndarray:
        quotes = numpy.array(
            [
                self.__market.getQuotes(underlying, self.__sampleWindow)
                for underlying in self.__underlyings
            ]
        )

        self.__checkNansRate(quotes)
        quotes = self.__removeNans(quotes)

        return numpy.diff(numpy.log(quotes), axis=1)

    def __getSampleCovarianceMatrix(self) -> None:
        if self.__covarianceMatrix is not None:
            return

        logReturns = self.__getLogChange()
        sampleLength = numpy.busday_count(
            self.__sampleWindow[0],
            self.__sampleWindow[-1]
        )
        self.__covarianceMatrix = logReturns @ logReturns.T / sampleLength

    def getObservationDate(self) -> date:
        return self.__observationDate

    def getTotalCovariance(self, forecastDate: date) -> numpy.ndarray:
        self.__getSampleCovarianceMatrix()

        forecastLength = numpy.busday_count(
            self.__observationDate,
            forecastDate
        )
        return self.__covarianceMatrix * forecastLength
