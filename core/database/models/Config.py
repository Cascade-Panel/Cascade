"""The Config model for application settings."""

import datetime
from typing import Any
import uuid
from sqlalchemy import Column, DateTime, String, Integer, Boolean
from core.database import Base

def gen_uuid() -> uuid.UUID:
    """Generate a new UUID."""
    return uuid.uuid4()

class Config(Base):
    """
    The Config model represents configuration settings.

    Attributes:
        id (int): The primary key for the configuration entry.
        key (str): The configuration key, identifying the setting.
        type (str): The type of the setting (e.g., 'boolean', 'string', 'integer').
        value (str): The value of the setting, stored as a string.
        created_on (datetime): The timestamp when the configuration entry was created.
        updated_on (datetime): The timestamp when the configuration entry was last updated.
    """
    __tablename__ = 'Config'

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, nullable=False, unique=True)
    type = Column(String, nullable=False)  # Type of setting (e.g., 'boolean', 'string', 'integer')
    value = Column(String, nullable=False)  # Value of the setting, set as string
    created_on = Column(DateTime, nullable=False, default=datetime.datetime.now())
    updated_on = Column(DateTime, nullable=False, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    @property
    def as_boolean(self) -> bool:
        """
            Return the value as a boolean if the type is 'boolean'.

            Returns:
                bool: The value of the setting as a boolean.
            
            Raises:
                ValueError: If the setting is not of type 'boolean'.
        """
        if self.type == 'boolean':
            return self.value.lower() in ['true', '1', 'yes', 'True']
        raise ValueError(f"Setting '{self.key}' is not of type 'boolean'.")

    @property
    def as_integer(self) -> int:
        """
            Return the value as an integer if the type is 'integer'.

            Returns:
                int: The value of the setting as an integer.
            
            Raises:
                ValueError: If the setting is not of type 'integer
        """
        if self.type == 'integer':
            return int(self.value)
        raise ValueError(f"Setting '{self.key}' is not of type 'integer'.")

    @property
    def as_string(self) -> str:
        """
            Return the value as a string.

            Returns:
                str: The value of the setting as a string.
            
            Raises:
                ValueError: If the setting is not of type 'string'.
        """
        if self.type == 'string':
            return self.value
        raise ValueError(f"Setting '{self.key}' is not of type 'string'.")

    def set_value(self, value: Any) -> None:
        """
        Set the value of the setting based on its type.
        
        Attributes:
            value (Any): The value to set for the setting.
        
        Raises:
            ValueError: If the value is not of the correct type.
        """
        if self.type == 'boolean':
            if not isinstance(value, bool):
                raise ValueError("Value must be a boolean.")
            self.value = 'true' if value else 'false'
        elif self.type == 'integer':
            if not isinstance(value, int):
                raise ValueError("Value must be an integer.")
            self.value = str(value)
        elif self.type == 'string':
            if not isinstance(value, str):
                raise ValueError("Value must be a string.")
            self.value = value
        else:
            raise ValueError(f"Unsupported setting type '{self.type}'.")

    def __repr__(self) -> str:
        return f"<Config(key={self.key}, type={self.type}, value={self.value})>"