from datetime import date
from unittest import TestCase

import numpy

from Products.QuoteProvider import QuoteProvider
from Simulation.FlatSampleCovarianceForecast import \
    FlatSampleCovarianceForecast

GAZPQuotes = {
    date(2021, 11, 1): 110,
    date(2022, 10, 28): 135,
    date(2022, 11, 1): 136,
}

YNDXQuotes = {
    date(2021, 11, 1): 140,
    date(2022, 10, 28): 155,
    date(2022, 10, 31): 145,
    date(2022, 11, 1): 155,
}


class QuoteProviderStub(QuoteProvider):
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


class FlatSampleCovarianceForecastTest(TestCase):
    def setUp(self) -> None:
        self.__testedException = FlatSampleCovarianceForecast(
            underlyings=['GAZP', 'YNDX'],
            observationDate=date(2022, 11, 1),
            samplelWindowSize=1,
            market=QuoteProviderStub(),
            missedQuotesLimit=0.3
        )
        self.__testedCovariance = FlatSampleCovarianceForecast(
            underlyings=['GAZP', 'YNDX'],
            observationDate=date(2022, 11, 1),
            samplelWindowSize=1,
            market=QuoteProviderStub(),
            missedQuotesLimit=1
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
            [0.04199522, 0.02084453],
            [0.02084453, 0.01035972]
        ])

        with self.subTest():
            numpy.testing.assert_allclose(
                sampleCovarianceMatrix * (1 / 365),
                self.__testedCovariance.getTotalCovariance(date(2022, 11, 2)),
                rtol=1e-5
            )

        with self.subTest():
            numpy.testing.assert_allclose(
                sampleCovarianceMatrix * (7 / 365),
                self.__testedCovariance.getTotalCovariance(date(2022, 11, 8)),
                rtol=1e-5
            )
