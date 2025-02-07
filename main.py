from strategy.fire_strategy import FireStrategy
from models.event import Event
from observer.skkm import SKKM
from iterator.concrete_aggregate import EventCollection
import time
from models.unit import Unit
#from simulate_events import simulate_events_fixed_location
from simulate_events import simulate_events
import threading

if __name__ == "__main__":
    # Define bounds and probabilities
    bounds = ((49.95855025648944, 19.688292482742394), (50.154564013341734, 20.02470275868903))
    probabilities = [0.3, 0.7]  # PZ: 30%, MZ: 70%

    fixed_location = (50.0614300, 19.9365800)  # Współrzędne JRG-1 diagnostykaa
    # Initialize SKKM
    skkm = SKKM()

    # Create units
    units = [
        Unit("JRG-1", 50.0614300, 19.9365800),          # ul. Westerplatte 19, Kraków
        Unit("JRG-2", 50.0400000, 19.9500000),          # ul. Rzemieślnicza 10, Kraków
        Unit("JRG-3", 50.0833330, 19.9000000),          # ul. Zarzecze 106, Kraków
        Unit("JRG-4", 50.0400000, 20.0000000),          # ul. Obrońców Modlina 2, Kraków
        Unit("JRG-5", 50.1000000, 19.9500000),          # ul. Kazimierza Wyki 3, Kraków
        Unit("JRG-6", 50.0200000, 20.0000000),          # ul. Aleksandry 2, Kraków
        Unit("JRG-7", 50.0700000, 19.9800000),          # ul. Rozrywka 26, Kraków
        Unit("JRG SA PSP", 50.0700000, 20.0400000),     # os. Zgody 18, Kraków
        Unit("JRG Skawina", 49.9800000, 19.8300000),    # ul. Piłsudskiego 79, Skawina
        Unit("LSP Balice", 50.0770000, 19.7840000)      # Lotnisko Balice, Balice
    ]


    # Add units as observers
    for unit in units:
        skkm.add_observer(unit)

    # Create a stop event for graceful shutdown
    stop_event = threading.Event()
            # Start event generation in a separate thread
    event_thread = threading.Thread(
            target=simulate_events,
            args=(skkm, bounds, probabilities, (1, 5), stop_event),
            daemon=True
        )
    event_thread.start()
    
    '''
    # Start generowania zdarzeń w stałej lokalizacji
    event_thread = threading.Thread(
        target=simulate_events_fixed_location,
        args=(skkm, fixed_location, probabilities, (1, 5), stop_event),
        daemon=True
    )
    event_thread.start()
    '''
    print("Simulation started.")
    time.sleep(5)
    try:
        while True:
            time.sleep(1)  # Main loop keeps running
    except KeyboardInterrupt:
        print("\nStopping simulation...")
        stop_event.set()  # Set the stop flag
        event_thread.join()  # Wait for the thread to finish
        print("Simulation stopped.")
