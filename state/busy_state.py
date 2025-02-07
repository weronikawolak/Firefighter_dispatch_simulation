from state.state import State

class BusyState(State):
    def handle(self, vehicle):
        vehicle.state = self  # Zmienia stan pojazdu na zajęty

    def __str__(self):
        return "Busy"
