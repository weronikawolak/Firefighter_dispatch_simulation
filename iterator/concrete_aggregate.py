import random
from iterator.iterator import Iterator
from iterator.concrete_iterator import EventIterator
from models.event import Event

class EventCollection:
    """
    Kolekcja generująca zdarzenia w oparciu o podane granice i prawdopodobieństwa.
    """
    def __init__(self, bounds, probabilities, event_count=10):
        self.bounds = bounds
        self.probabilities = probabilities
        self.event_count = event_count
        self.events = self._generate_events()

    def _generate_events(self):
        """
        Generuje kolekcję zdarzeń w oparciu o granice i prawdopodobieństwa.
        """
        (lat_min, lon_min), (lat_max, lon_max) = self.bounds
        events = []

        for _ in range(self.event_count):
            latitude = random.uniform(lat_min, lat_max)
            longitude = random.uniform(lon_min, lon_max)
            event_type = random.choices(["PZ", "MZ"], weights=self.probabilities)[0]
            events.append(Event(event_type, (latitude, longitude)))

        return events

    def iterator(self):
        """
        Zwraca iterator dla kolekcji zdarzeń.
        """
        return EventIterator(self.bounds, self.probabilities, self.event_count)
