from abc import ABC, abstractmethod

class Aggregate(ABC):
    @abstractmethod
    def iterator(self):
        """
        Tworzy i zwraca obiekt iteratora.
        """
        pass
