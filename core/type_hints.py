""" This module contains custom type validators. """

import re

class Email:
    """
        A class representing an email address.
        - Conforms to the [RFC 5322](https://datatracker.ietf.org/doc/html/rfc5322) standard.

        Attributes:
            address (str): The email address.
        
        Raises:
            ValueError: If the address is not a valid email address.
    """
    def __init__(self, address: str):
        if not self._is_valid(address):
            raise ValueError(f"Invalid email address: {address}")
        self.address = address

    _pattern = re.compile(
        r"^(?:[a-zA-Z0-9_'^&/+-])+(?:\.[a-zA-Z0-9_'^&/+-]+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
    )

    @classmethod
    def _is_valid(cls, address: str) -> bool:
        return bool(cls._pattern.match(address))

    def __str__(self) -> str:
        return self.address

    def __repr__(self) -> str:
        return f"Email('{self.address}')"

class Password:
    """
        A class representing a password.
        - Must be at least 8 characters long.
        - Must contain at least one uppercase letter.
        - Must contain at least one lowercase letter.
        - Must contain at least one digit.
        - Must contain at least one special character.

        Attributes:
            password (str): The password.
        
        Raises:
            ValueError: If the password is not a valid password.
    """
    def __init__(self, password: str):
        if not self._is_valid(password):
            raise ValueError("Invalid password.")
        self.password = password

    _pattern = re.compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    )

    @classmethod
    def _is_valid(cls, password: str) -> bool:
        return bool(cls._pattern.match(password))

    def __str__(self) -> str:
        return self.password

    def __repr__(self) -> str:
        return f"Password('{self.password}')"

