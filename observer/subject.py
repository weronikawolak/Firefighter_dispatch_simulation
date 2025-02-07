#zarzadza kolekcja obserwatorow

class ObservedSubject:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        """
        Dodaje obserwatora do listy subskrybentów.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        """
        Usuwa obserwatora z listy subskrybentów.
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observer(self, observer, data):
        """
        Powiadamia konkretnego obserwatora.
        """
        if observer in self._observers:
            observer.update(data)

    def notify_all(self, data):
        """
        Powiadamia wszystkich obserwatorów.
        """
        for observer in self._observers:
            observer.update(data)
