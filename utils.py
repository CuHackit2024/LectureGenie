
class ProgressUpdate:
    """
    A class that represents a progress update
    """
    def __init__(self, progress: float, message: str):
        """
        A class that represents a progress update
        :param progress:  A float between 0 and 1 that represents the progress
        :param message: A message to display with the progress
        """
        self.progress = progress
        self.message = message

    def __str__(self):
        return f"Progress: {self.progress * 100:.2f}% - {self.message}"