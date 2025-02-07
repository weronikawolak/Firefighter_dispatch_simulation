
#from generate_event import generate_event

from threading import Event
import random
import time
from models.event import Event
from iterator.concrete_aggregate import EventCollection


from threading import Thread
from iterator.concrete_iterator import EventIterator


def simulate_events(skkm, bounds, probabilities, interval_range=(1, 5), stop_event=None):
    """
    Generates events in the background within the specified bounds at random intervals.
    Stops when stop_event is set.
    """
    event_collection = EventCollection(bounds, probabilities)

    while not stop_event.is_set():
        iterator = event_collection.iterator()

        while iterator.has_next() and not stop_event.is_set():
            event = iterator.next()
            skkm.add_event(event)
            time.sleep(random.uniform(*interval_range))

        # Restart the iterator or break based on use case
        if not stop_event.is_set():
            # Optionally reset the iterator if you want infinite generation
            # event_collection.reset()
            print("No more events in the current batch. Waiting...")
            time.sleep(5)  # Wait before retrying

'''
def simulate_events_fixed_location(skkm, fixed_location, probabilities, interval_range=(1, 5), stop_event=None):
    """
    Generuje zdarzenia w stałej lokalizacji w tle z określonymi interwałami.
    Args:
        skkm: Obiekt SKKM.
        fixed_location: Stałe współrzędne lokalizacji (latitude, longitude).
        probabilities: Prawdopodobieństwa wystąpienia typów zdarzeń.
        interval_range: Zakres czasu w sekundach między zdarzeniami.
        stop_event: Obiekt threading.Event do kontrolowania zatrzymania.
    """
    while not stop_event.is_set():
        # Stała lokalizacja zdarzenia
        latitude, longitude = fixed_location

        # Losowy typ zdarzenia
        event_type = random.choices(["PZ", "MZ"], weights=probabilities)[0]

        # Utwórz zdarzenie
        event = Event(event_type, (latitude, longitude))
        skkm.add_event(event)

        # Czekaj losowy czas przed generowaniem następnego zdarzenia
        time.sleep(random.uniform(*interval_range))
'''