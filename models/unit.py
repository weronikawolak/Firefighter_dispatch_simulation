import math
import time
import random
from threading import Thread, Lock
import logging
from strategy.base_strategy import IStrategy
from observer.observer import Observer
from state.free_state import FreeState
from state.busy_state import BusyState
from utilis.log_event import log_event

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class Vehicle:
    """
    Klasa reprezentująca pojedynczy pojazd.
    """
    def __init__(self, id, unit):
        self.id = id
        self.state = FreeState()
        self.unit = unit  # Assign the parent unit

    def set_state(self, state):
        """
        Zmienia stan pojazdu i loguje zmianę.
        """
        self.state = state

    def is_free(self):
        return isinstance(self.state, FreeState)

    def __str__(self):
        return f"Vehicle {self.id} ({'Busy' if isinstance(self.state, BusyState) else 'Free'})"

class Unit(Observer):
    """
    Klasa reprezentująca jednostkę straży pożarnej.
    """
    def __init__(self, name, latitude, longitude, strategy: IStrategy = None, vehicle_count=5):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.strategy = strategy  # Strategia domyślnie None
        self.vehicles = [Vehicle(i, self) for i in range(vehicle_count)]  # Pass `self` to Vehicle
        self.bounds = None  # Zakres działania jednostki
        self.lock = Lock()  # Blokada do synchronizacji dostępu

    def update(self, event):
        if self.strategy is None:
            logger.warning(f"Unit {self.name} does not have a strategy set and cannot handle the event.")
            return

        # Delegacja obsługi zdarzenia do strategii
        Thread(target=self.strategy.execute, args=(self, event), daemon=True).start()

    def set_bounds(self, bounds):
        self.bounds = bounds

    def is_within_bounds(self, location):
        if not self.bounds:
            return True  # Jeśli brak ograniczeń, zawsze w zakresie
        (lat_min, lon_min), (lat_max, lon_max) = self.bounds
        lat, lon = location
        return lat_min <= lat <= lat_max and lon_min <= lon <= lon_max

    def display_vehicle_states(self):
        """
        Displays the current states of all vehicles in a simplified format.
        """
        states = ["Busy" if isinstance(vehicle.state, BusyState) else "Free" for vehicle in self.vehicles]
        print(f"Unit {self.name} Vehicle States: {states}")

    def calculate_distance(self, location):
        lat1, lon1 = self.latitude, self.longitude
        lat2, lon2 = location

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)

        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        r = 6371
        return r * c

    def has_free_vehicles_count(self):
        """
        Zwraca liczbę wolnych pojazdów w jednostce.
        """
        return len([v for v in self.vehicles if v.is_free()])
