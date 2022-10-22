from abc import ABC, abstractmethod
from typing import Tuple


class Matrix(ABC):
    @abstractmethod
    def __getitem__(self, *args: Tuple[int, int]):
        pass
