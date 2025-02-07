from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def handle(self, vehicle):
        """
        Obsługuje zmianę stanu pojazdu.
        """
        pass

    @abstractmethod
    def __str__(self):
        """
        Zwraca nazwę stanu.
        """
        pass
