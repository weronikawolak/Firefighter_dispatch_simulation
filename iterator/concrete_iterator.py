from iterator.iterator import Iterator
from models.event import Event
import random

class EventIterator(Iterator):
    """
    Konkretna implementacja iteratora dla zdarzeń.
    """
    def __init__(self, bounds, probabilities, event_count=None):
        """
        Args:
            bounds: Granice prostokąta ((lat_min, lon_min), (lat_max, lon_max)).
            probabilities: Prawdopodobieństwa zdarzeń (np. [0.3, 0.7]).
            event_count: Liczba zdarzeń do wygenerowania (None dla nieskończonej iteracji).
        """
        self.bounds = bounds
        self.probabilities = probabilities
        self.event_count = event_count
        self.current = 0

    def has_next(self) -> bool:
        """
        Sprawdza, czy są jeszcze zdarzenia do wygenerowania.
        """
        return self.event_count is None or self.current < self.event_count


    def next(self):
        """
        Generuje i zwraca kolejne zdarzenie.
        """
        if not self.has_next():
            raise StopIteration("No more events.")

        (lat_min, lon_min), (lat_max, lon_max) = self.bounds

        # Losowe współrzędne
        latitude = random.uniform(lat_min, lat_max)
        longitude = random.uniform(lon_min, lon_max)

        # Losowy typ zdarzenia
        event_type = random.choices(["PZ", "MZ"], weights=self.probabilities)[0]

        self.current += 1
        return Event(event_type, (latitude, longitude))
