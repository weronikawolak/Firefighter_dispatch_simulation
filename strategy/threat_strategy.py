import time
import random
import logging
from threading import Thread
from state.free_state import FreeState
from state.busy_state import BusyState
from strategy.base_strategy import IStrategy

# Logger settings for better readability
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)



class ThreatStrategy(IStrategy):
    """
    Strategy for handling local threat events.
    """

    def required_vehicles(self):
        return 2  # Number of vehicles needed for a threat event

    def execute(self, unit, event):
        needed_vehicles = self.required_vehicles()
        logger.info(f"⚠️ [Threat] Event detected. Dispatching {needed_vehicles} vehicles from unit: {unit.name}")
        self._dispatch_and_simulate(unit, needed_vehicles, event)

    def _dispatch_and_simulate(self, unit, count, event):
        with unit.lock:
            free_vehicles = [v for v in unit.vehicles if v.is_free()]
            dispatched = []

            if len(free_vehicles) >= count:
                for vehicle in free_vehicles[:count]:
                    vehicle.set_state(BusyState())
                    dispatched.append(vehicle)
                logger.info(f"🚒 Dispatched {len(dispatched)} vehicles for threat event ID: {event.id}.")
            else:
                for vehicle in free_vehicles:
                    vehicle.set_state(BusyState())
                    dispatched.append(vehicle)

            unit.display_vehicle_states()

            Thread(target=self._simulate_action, args=(unit, dispatched, event), daemon=True).start()

    def _simulate_action(self, unit, vehicles, event):
        travel_time = random.randint(0, 3)
        logger.info(f"🚦 Vehicles en route to threat event ID: {event.id}. Travel time: {travel_time}s.")
        time.sleep(travel_time)

        # Check for false alarm
        if random.random() < 0.05:  # 5% chance of false alarm
            logger.info(f"🚨 False alarm for threat event ID: {event.id}. Vehicles are returning to base.")
            return_time = random.randint(0, 3)
            logger.info(f"🔙 Vehicles returning from false alarm. Return time: {return_time}s.")
            time.sleep(return_time)

            with unit.lock:
                for vehicle in vehicles:
                    vehicle.set_state(FreeState())
            logger.info(f"✅ Vehicles returned to base after false alarm for threat event ID: {event.id}.")
            return

        action_time = random.randint(5, 25)
        logger.info(f"⚠️ Handling threat event ID: {event.id}. Estimated duration: {action_time}s.")
        time.sleep(action_time)

        return_time = random.randint(0, 3)
        logger.info(f"🔙 Vehicles returning from threat event ID: {event.id}. Return time: {return_time}s.")
        time.sleep(return_time)

        with unit.lock:
            for vehicle in vehicles:
                vehicle.set_state(FreeState())
        logger.info(f"✅ Vehicles returned to base after handling threat event ID: {event.id}.")
