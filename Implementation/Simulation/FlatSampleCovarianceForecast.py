from datetime import date
from typing import List

import numpy
from dateutil.relativedelta import relativedelta
from dateutil.rrule import DAILY, rrule

from Products.QuoteProvider import QuoteProvider
from Simulation.CovarianceTermStructure import CovarianceTermStructure


class FlatSampleCovarianceForecast(CovarianceTermStructure):
    def __init__(
        self,
        underlyings: List[str],
        observationDate: date,
        samplelWindowSize: int,
        market: QuoteProvider,
        missedQuotesLimit: float = 0.3
    ):
        """
        missedQuotesLimit: The maximum percentage of missed quotes. If there
        are more missing quotes that this rate, the function throws an
        exception.
        """
        self.__underlyings = underlyings
        self.__observationDate = observationDate
        self.__market = market
        self.__sampleWindow = [
            sampleDate.date() for sampleDate in rrule(
                DAILY,
                dtstart=observationDate - relativedelta(
                    years=samplelWindowSize
                ),
                until=observationDate,
                byweekday=(0, 1, 2, 3, 4)
            )
        ]
        self.__sampleQuotes = None
        self.__missedQuotesLimit = missedQuotesLimit
        self.__covarianceMatrix = None

    def __checkMissedQuotesRate(self) -> None:
        if (
            (self.__sampleQuotes == numpy.array(None)).all(axis=0).sum() >=
            int(self.__missedQuotesLimit * self.__sampleQuotes.shape[1])
        ):
            raise ValueError(
                'The percentage of missed quotes is higher than '
                'missedQuotesLimit parameter.'
            )

    def __removeMissedQuotes(self) -> None:
        indicesToDelete = (
            self.__sampleQuotes == numpy.array(None)
        ).any(axis=0)

        self.__sampleWindow = numpy.delete(
            self.__sampleWindow,
            indicesToDelete
        )
        self.__sampleQuotes = numpy.delete(
            self.__sampleQuotes, indicesToDelete, axis=1
        ).astype(float)

    def __getLogReturns(self) -> numpy.ndarray:
        self.__sampleQuotes = numpy.array(
            [
                self.__market.getQuotes(underlying, self.__sampleWindow)
                for underlying in self.__underlyings
            ]
        )

        self.__checkMissedQuotesRate()
        self.__removeMissedQuotes()

        return numpy.diff(numpy.log(self.__sampleQuotes), axis=1)

    def __calculateSampleCovarianceMatrix(self) -> None:
        if self.__covarianceMatrix is not None:
            return

        logReturns = self.__getLogReturns()
        sampleLength = (
                            self.__sampleWindow[-1] - self.__sampleWindow[0]
                       ).days / 365
        self.__covarianceMatrix = logReturns @ logReturns.T / sampleLength

    def getObservationDate(self) -> date:
        return self.__observationDate

    def getTotalCovariance(self, forecastDate: date) -> numpy.ndarray:
        self.__calculateSampleCovarianceMatrix()

        forecastLength = (forecastDate - self.__observationDate).days / 365

        return self.__covarianceMatrix * forecastLength
