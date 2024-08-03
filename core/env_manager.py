""" Self-contained .env manager for the application. Allows for updates and retrieval of .env values. """

import os
from typing import Any, Union
from sanic import json

class EnvManager:
    """ EnvManager class for managing .env values. """

    def __init__(self) -> None:
        """
            Initialize the EnvManager class.

            Attributes:
                env_file (str): Path to the .env file.
                env_values (dict): Dictionary of .env values.
        """
        self.env_file = os.path.join(os.path.dirname(__file__), ".env")
        self.env_values = self.load_env()

    def load_env(self) -> dict:
        """
            Load .env file into a dictionary.
            
            Returns:
                dict: Dictionary of .env values.
        """
        env_values = {}
        if not os.path.exists(self.env_file):
            return env_values
        
        with open(self.env_file, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_values[key.strip()] = self._cast_value(value.strip())
        
        return env_values

    def _cast_value(self, value: str) -> Any:
        """
            Cast value to its appropriate type.
            
            Args:
                value (str): The value to cast.
            
            Returns:
                Any: The casted value.
        """
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            pass
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        if value.startswith('[') and value.endswith(']'):
            return [self._cast_value(item.strip()) for item in value[1:-1].split(',')]
        if value.startswith('{') and value.endswith('}'):
            return {item.split(':')[0].strip(): self._cast_value(item.split(':')[1].strip()) for item in value[1:-1].split(',')}
        return value

    def get(self, key: str) -> Union[str, int, list, dict, float, bool, None]:
        """
            Get a value from the .env file.

            Args:
                key (str): Key to get value for.
            
            Returns:
                Union[str, int, list, dict, float, bool, None]: Value for the key.
        """
        return self.env_values.get(key)

    def set(self, key: str, value: Union[str, int, list, dict, float, bool]) -> None:
        """
            Set a value in the .env file.

            Args:
                key (str): Key to set value for.
                value (Union[str, int, list, dict, float, bool]): Value to set for the key.
        """
        self.env_values[key] = value
        self.__save_env__()

    def __save_env__(self) -> None:
        """
            Save the .env values to the .env file.
        """
        with open(self.env_file, "w") as file:
            for key, value in self.env_values.items():
                file.write(f"{key}={self._value_to_string(value)}\n")

    def _value_to_string(self, value: Any) -> str:
        """
            Convert a value to its string representation.

            Args:
                value (Any): The value to convert.
            
            Returns:
                str: The string representation of the value.
        """
        if isinstance(value, (list, dict)):
            return json.dumps(value)
        return str(value)
