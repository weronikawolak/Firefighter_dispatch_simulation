from abc import ABC, abstractmethod

class Iterator(ABC):
    @abstractmethod
    def has_next(self) -> bool:
        """
        Sprawdza, czy kolekcja zawiera następny element.
        """
        pass

    @abstractmethod
    def next(self):
        """
        Zwraca następny element w kolekcji.
        """
        pass
