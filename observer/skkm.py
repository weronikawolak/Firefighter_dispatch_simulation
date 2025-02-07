from observer.subject import ObservedSubject
from threading import Thread
from strategy.base_strategy import IStrategy
from strategy.fire_strategy import FireStrategy
from strategy.threat_strategy import ThreatStrategy
from state.free_state import FreeState
from state.busy_state import BusyState
import logging

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class SKKM(ObservedSubject):
    def __init__(self):
        super().__init__()
        self.events = []
        self.event_counter = {"PZ": 0, "MZ": 0}  # Counter for readable incident IDs
        self.strategies = {
            "PZ": FireStrategy(),
            "MZ": ThreatStrategy()
        }
        self.current_strategy = None

    def set_strategy(self, event_type: str):
        self.current_strategy = self.strategies.get(event_type)

    def generate_readable_id(self, event_type):
        self.event_counter[event_type] += 1
        return f"Incident-{event_type}-{self.event_counter[event_type]:03d}"

    def add_event(self, event):
        """
        Dodaje zdarzenie i powiadamia jednostki.
        """
        event.id = self.generate_readable_id(event.event_type)  # Assign readable ID
        self.events.append(event)
        print(f"SKKM: New event ({event.event_type}) - ID: {event.id}, Location: {event.location}")
        self.set_strategy(event.event_type)
        Thread(target=self.notify_closest_units, args=(event,), daemon=True).start()

    def notify_closest_units(self, event):
        available_units = [unit for unit in self._observers if unit.has_free_vehicles_count() > 0]
        if not available_units:
            print(f"[SKKM] Event {event.id}: No free vehicles for event {event.event_type} at {event.location}.")
            return

        if not self.current_strategy:
            print(f"[SKKM] Event {event.id}: No strategy set for handling the event.")
            return

        remaining_vehicles = self.current_strategy.required_vehicles()

        for unit in sorted(available_units, key=lambda u: u.calculate_distance(event.location)):
            if remaining_vehicles <= 0:
                break

            free_count = unit.has_free_vehicles_count()
            to_dispatch = min(free_count, remaining_vehicles)

            if to_dispatch > 0:
                logger.info(f"Dispatching {to_dispatch} vehicles from unit {unit.name}.")
                self.current_strategy._dispatch_and_simulate(unit, to_dispatch, event)
                remaining_vehicles -= to_dispatch

        if remaining_vehicles > 0:
            print(f"[SKKM] Event {event.id}: Could not dispatch all required vehicles. Missing: {remaining_vehicles}.")
        else:
            print(f"[SKKM] Event {event.id}: Fully dispatched with required vehicles.")

    def display_vehicle_states(self, units):
        """
        Display states of vehicles for all units in a structured format.
        """
        for unit in units:
            states = ["Busy" if isinstance(vehicle.state, BusyState) else "Free" for vehicle in unit.vehicles]
            print(f"\n{'='*50}")
            print(f"Unit {unit.name} Vehicle States")
            print(f"{'-'*50}")
            print(f"States: {' | '.join(states)}")
            print(f"{'='*50}\n")
