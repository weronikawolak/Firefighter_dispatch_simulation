from abc import ABC, abstractmethod

class IStrategy(ABC):
    @abstractmethod
    def execute(self, unit, event):
        """
        Zwraca liczbę pojazdów potrzebnych do obsługi zdarzenia.
        """
        pass