def log_event(message, unit_name=None):
    """
    Wypisuje sformatowaną wiadomość w przyjemnym dla użytkownika stylu.
    """
    if unit_name:
        print(f"[{unit_name}] {message}")
    else:
        print(f"{message}")
