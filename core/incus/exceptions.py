# incus_sdk/exceptions.py

class IncusAPIError(Exception):
    """Exception raised for errors in the Incus API."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class IncusClientError(Exception):
    """Exception raised for errors in the Incus client."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)