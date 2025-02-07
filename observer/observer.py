from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, data):
        """
        Powiadomienie obserwatora o zmianie stanu.
        """
        pass
