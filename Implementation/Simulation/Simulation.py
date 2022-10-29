from abc import ABC, abstractmethod
from datetime import date


class Simulation(ABC):
    @abstractmethod
    def getSimulatedValue(
        self,
        variableName: str,
        simulationDate: date,
        simulationIndex: int
    ) -> float:
        pass
