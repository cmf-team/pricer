from datetime import date
from typing import List

import numpy

from Simulation.CovarianceTermStructure import CovarianceTermStructure
from Simulation.DiscountCurve import DiscountCurve
from Simulation.Simulation import Simulation


class GeometricBrownianMotion(Simulation):
    def __init__(
        self,
        variableNames: List[str],
        observationDate: date,
        simulationDates: List[date],
        initialValues: List[float],
        drift: List[DiscountCurve],
        covariance: CovarianceTermStructure,
        simulationNumber: int
    ):
        self.__variableNames = variableNames
        self.__observationDate = observationDate
        self.__simulationDates = simulationDates
        self.__initialValues = initialValues
        self.__drift = drift
        self.__covariance = covariance
        self.__simulationNumber = simulationNumber
        self.__simulationResult = None

        self.__muValues = self.__getMuValues()
        self.__sigmaValues = self.__getSigmaValues()

        self.__brownianMotionStep(
            mu=self.__muValues[:, 0],
            sigma=self.__sigmaValues[:, 0],
            T1=self.__simulationDates[0],
            T2=self.__simulationDates[1]
        )

    def __brownianMotionStep(self, mu, sigma, T1, T2):
        d = len(self.__variableNames)

        initValues = numpy.reshape(
            numpy.asarray(self.__initialValues), [1, d]
        )

        path = numpy.exp(
            (mu - sigma / 2) + numpy.random.multivariate_normal(
                mean=numpy.zeros(d),
                cov=self.__getRandomCovariance(T1, T2),
                size=self.__simulationNumber
            )
        )
        return initValues * path

    def __getMuValues(self):
        discountFactors = []
        for discountCurve in self.__drift:
            discountFactors = [discountCurve.getDiscountFactor(simulationDate)
                for simulationDate in self.__simulationDates
            ]
        discountFactors = numpy.array(discountFactors)
        discountFactorsDiv = discountFactors[:-1] / discountFactors[1:]
        return numpy.array(discountFactorsDiv)

    def __getSigmaValues(self):
        variablesNumber = len(self.__variableNames)
        totalCovarianceValues = []
        for simulationDate in self.__simulationDates:
            C = self.__covariance.getTotalCovariance(
                forecastDate=simulationDate
            )
            simulationDateCovariance = []
            for idx in range(variablesNumber):
                simulationDateCovariance.append(C[idx, idx])
        totalCovarianceValues.append(simulationDateCovariance)
        totalCovarianceValues = numpy.array(totalCovarianceValues)
        return numpy.diff(totalCovarianceValues, axis=0)

    def __getRandomCovariance(self, firstDate, secondDate):
        C1 = self.__covariance.getTotalCovariance(firstDate)
        C2 = self.__covariance.getTotalCovariance(secondDate)
        return C2 - C1

    def getSimulatedValue(
        self,
        variableName: str,
        simulationDate: date,
        simulationIndex: int
    ) -> float:
        variableIndex = self.__variableNames.index(variableName)
        return self.__simulationResult[variableIndex][simulationIndex][
            simulationDate
        ]
