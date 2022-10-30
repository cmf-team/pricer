from datetime import date
from unittest import TestCase

import numpy

from Products.QuoteProvider import QuoteProvider
from Simulation.FlatHistoricalCovarianceForecast import \
    FlatSampleCovarianceForecast

GAZPQuotes = {
    date(2022, 10, 27): 100,
    date(2022, 10, 28): 105,
    date(2022, 10, 31): numpy.NaN,
    date(2022, 11, 1): 106,
}

YNDXQuotes = {
    date(2022, 10, 27): 150,
    date(2022, 10, 28): 130,
    date(2022, 10, 31): 155,
    date(2022, 11, 1): 155,
}

YNDXQuotesExceptions = {
    date(2022, 10, 27): 150,
    date(2022, 10, 28): numpy.NaN,
    date(2022, 10, 31): numpy.NaN,
    date(2022, 11, 1): 155,
}


class QuoteProviderStub(QuoteProvider):
    def __init__(self, exception: bool = False):
        self.__GAZPQuotes = GAZPQuotes
        if exception:
            self.__YNDXQuotes = YNDXQuotesExceptions
        else:
            self.__YNDXQuotes = YNDXQuotes

    def getQuotes(
        self,
        ticker: str,
        observationDates: list[date]
    ) -> list[float]:

        if ticker == "GAZP":
            try:
                return [
                    self.__GAZPQuotes.get(observationDate) for
                    observationDate in observationDates
                ]
            except KeyError:
                raise NotImplementedError()

        if ticker == "YNDX":
            try:
                return [
                    self.__YNDXQuotes.get(observationDate) for
                    observationDate in observationDates
                ]
            except KeyError:
                raise NotImplementedError()


class AutocallTest(TestCase):
    def setUp(self) -> None:
        self.__testedCovariance = FlatSampleCovarianceForecast(
            underlyings=['GAZP', 'YNDX'],
            observationDate=date(2022, 11, 1),
            samplelWindowSize=4,
            market=QuoteProviderStub(),
            missedQuotesLimit=0.3
        )
        self.__testedException = FlatSampleCovarianceForecast(
            underlyings=['GAZP', 'YNDX'],
            observationDate=date(2022, 11, 1),
            samplelWindowSize=4,
            market=QuoteProviderStub(exception=True),
            missedQuotesLimit=0.3
        )

    def testGetObservationDate(self):
        self.assertEqual(
            date(2022, 11, 1),
            self.__testedCovariance.getObservationDate()
        )

    def testException(self):
        with self.assertRaises(ValueError):
            self.__testedException.getTotalCovariance(date(2022, 11, 5))

    def testGetTotalCovariance(self):
        sampleCovarianceMatrix = numpy.array([
            [0.00082344, -0.00177156],
            [-0.00177156, 0.01713846]
        ])

        with self.subTest():
            numpy.testing.assert_allclose(
                sampleCovarianceMatrix,
                self.__testedCovariance.getTotalCovariance(date(2022, 11, 2)),
                rtol=1e-5
            )

        with self.subTest():
            numpy.testing.assert_allclose(
                sampleCovarianceMatrix * 5,
                self.__testedCovariance.getTotalCovariance(date(2022, 11, 8)),
                rtol=1e-5
            )
