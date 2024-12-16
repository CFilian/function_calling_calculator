class History:
    def __init__(self):
        self.history = []

    def add_entry(self, command, result):
        """Add a calculation entry to the history."""
        self.history.append(f"{command} = {result}")

    def get_all(self):
        """Retrieve all calculation history."""
        return self.history
