"""
This module provides the data-access-layer for managing config variables in the database.
"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.database.models.Config import Config
from core.database.DALs.base import BaseDAL
from core.type_hints import Email

class ConfigDAL(BaseDAL):
    """
        Data Access Layer for managing config variables in the database.

        Attributes:
            db_session (Session): The database session.
    """

    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
    
    async def new(self, key: str, value: str | int | bool, type: str) -> Config:
        """
            Add a new config variable to the database.

            Attributes:
                key (str): The key of the config variable.
                value (str | int | bool): The value of the config variable.
                type (str): The type of the config variable.
            
            Returns:
                Config: The config variable that was added to the database.
        """
        if type.lower() not in ['str', 'int', 'bool']:
            raise ValueError('Invalid type: {}'.format(type))

        config = Config(key=key, value=str(value), type=type.lower())
        self.db_session.add(config)
        self.db_session.commit()
        self.db_session.refresh(config)
        return config
    
    async def get(self, key: str) -> str | None:
        """
        Retrieve the value of a config variable from the database.

        Attributes:
            key (str): The key of the config variable to retrieve.
        
        Returns:
            str | None: The value of the config variable with the specified key, or None if not found
        """
        return self.db_session.query(Config.value).filter(Config.key == key).first()
    
    async def update(self, key: str, value: str | int | bool) -> Config:
        """
            Update the value of a config variable in the database.

            Attributes:
                key (str): The key of the config variable to update.
                value (str | int | bool): The new value of the config variable.
            
            Returns:
                Config: The updated config variable.
        """
        config = self.db_session.query(Config).filter(Config.key == key).first()
        if not config:
            raise ValueError('Config variable not found: {}'.format(key))
        
        config.value = str(value)
        self.db_session.commit()
        self.db_session.refresh(config)
        return config
    
    async def delete(self, key: str) -> None:
        """
            Remove a config variable from the database.

            Attributes:
                key (str): The key of the config variable to remove.
        """
        config = self.db_session.query(Config).filter(Config.key == key).first()
        if not config:
            raise ValueError('Config variable not found: {}'.format(key))
        
        self.db_session.delete(config)
        self.db_session.commit()