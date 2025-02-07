import uuid

class Event:
    def __init__(self, event_type, location):
        self.id = str(uuid.uuid4())[:8]  # Generujemy krótki identyfikator
        self.event_type = event_type
        self.location = location

    def __str__(self):
        return f"Danger {self.id} ({self.event_type}) in localization: {self.location}"
