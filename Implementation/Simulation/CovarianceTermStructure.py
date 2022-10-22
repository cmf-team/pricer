from abc import ABC, abstractmethod
from datetime import date

from Simulation.Matrix import Matrix


class CovarianceTermStructure(ABC):
    @abstractmethod
    def getObservationDate(self) -> date:
        pass

    @abstractmethod
    def getTotalCovariance(self, forecastDate: date) -> Matrix:
        pass
