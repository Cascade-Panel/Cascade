""" Self-contained .env manager for the application. Allows for updates and retrieval of .env values. """

import json
import os
import sys

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
    
    def load_env(self) -> dict | FileNotFoundError:
        """
            Load .env file into a dictionary.
            
            Returns:
                dict: Dictionary of .env values.
            
            Raises:
                FileNotFoundError: If no .env file is found
        """
        if not os.path.exists(self.env_file):
            raise FileNotFoundError("No .env file found.")

        with open(self.env_file, "r") as file:
            return json.load(file)
    
    def get(self, key: str) -> str | int | list | tuple | dict | float | None:
        """
            Get a value from the .env file.

            Args:
                key (str): Key to get value for.
            
            Returns:
                str | int | list | tuple | dict | None: Value for the key.
        """
        return self.env_values.get(key)
    
    def set(self, key: str, value: str | int | list | tuple | dict | float) -> None:
        """
            Set a value in the .env file.

            Args:
                key (str): Key to set value for.
                value (str | int | list | tuple | dict | float): Value to set for the key.
        """
        self.env_values[key] = value
        self.__save_env__()
    
    def __save_env__(self) -> None:
        """
            Save the .env values to the .env file.

            Raises:
                FileNotFoundError: If no .env file is found
        """
        with open(self.env_file, "w") as file:
            json.dump(self.env_values, file, indent=4)