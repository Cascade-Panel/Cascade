""" A collection of utility functions. """

import datetime
import json
from typing import Any
from uuid import UUID

class CustomEncoder(json.JSONEncoder):
    """
    JSON encoder that handles UUID, date, and datetime objects.
    """
    def default(self, o: object) -> Any:
        if isinstance(o, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(o)
        if isinstance(o, (datetime.date, datetime)):
            return o.isoformat()
        if isinstance(o, bytes):
            return o.decode('utf-8')  # or 'latin-1' or 'iso-8859-1' depending on your data - we use utf-8 (if it is changed, change here)

        return super().default(o)

def cleanse_dict(dictionary: dict) -> dict:
    """
    Fixes a dictionary by converting it to a JSON string and then parsing it back to a dictionary.

    Args:
        dictionary (dict): The dictionary to be fixed.

    Returns:
        dict: The fixed dictionary.
    """
    first = json.dumps(dictionary, cls=CustomEncoder)
    return json.loads(first)