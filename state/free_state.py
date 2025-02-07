from state.state import State

class FreeState(State):
    def handle(self, vehicle):
        vehicle.state = self  # Zmienia stan pojazdu na wolny

    def __str__(self):
        return "Free"
