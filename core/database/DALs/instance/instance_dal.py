"""
This module provides the data-access-layer for managing Instance records in the database.
"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.database.models.instance.Instance import Instance
from core.database.DALs.base import BaseDAL

class InstanceDAL(BaseDAL):
    """
    Data Access Layer for managing Instance records in the database.

    Args:
        db_session (Session): The database session.
    """
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
    
    async def new(self, instance: Instance) -> Instance:
        """
        Add a new Instance record to the database.

        Args:
            instance (Instance): The Instance record to add to the database.
        
        Returns:
            Instance: The Instance record that was added to the database.
        """
        self.db_session.add(instance)
        self.db_session.commit()
        self.db_session.refresh(instance)
        return instance
    
    async def get_by_incus_uuid(self, incus_uuid: UUID) -> Instance | None:
        """
        Retrieve an Instance record from the database by incus UUID.

        Args:
            incus_uuid (UUID): The incus UUID to retrieve the Instance record for.
        
        Returns:
            Instance | None: The Instance record with the specified incus UUID, or None if not found.
        """
        return self.db_session.query(Instance).filter(Instance.incus_uuid == incus_uuid).first()

    async def get_by_name(self, name: str) -> Instance | None:
        """
        Retrieve an Instance record from the database by name.

        Args:
            name (str): The name to retrieve the Instance record for.
        
        Returns:
            Instance | None: The Instance record with the specified name, or None if not found.
        """
        return self.db_session.query(Instance).filter(Instance.name == name).first()

    async def update(self, instance: Instance) -> Instance:
        """
        Update an Instance record in the database.

        Args:
            instance (Instance): The Instance record to update in the database.
        
        Returns:
            Instance: The Instance record that was updated in the database.
        """
        self.db_session.commit()
        self.db_session.refresh(instance)
        return instance
    
    async def refresh(self, instance: Instance) -> Instance:
        """
        Refresh an instance of an Instance record object from the database.

        Args:
            instance (Instance): The Instance record object to refresh.
        
        Returns:
            Instance: The Instance record that was refreshed in the database.
        """
        self.db_session.refresh(instance)
        return instance

    async def delete(self, instance: Instance) -> Instance:
        """
        Delete an Instance record from the database.

        Args:
            instance (Instance): The Instance record to delete from the database.
        
        Returns:
            Instance: The Instance record that was deleted from the database.
        """
        self.db_session.delete(instance)
        self.db_session.commit()
        return instance
    
    async def get_all(self) -> list[Instance]:
        """
        Retrieve all Instance records from the database.

        Returns:
            list[Instance]: A list of all Instance records in the database.
        """
        return self.db_session.query(Instance).all()

    async def get_by_owner_uuid(self, owner_uuid: UUID) -> list[Instance]:
        """
        Retrieve all Instance records from the database by owner UUID.

        Args:
            owner_uuid (UUID): The owner UUID to retrieve the Instance records for.
        
        Returns:
            list[Instance]: A list of all Instance records with the specified owner UUID.
        """
        return self.db_session.query(Instance).filter(Instance.owner_uuid == owner_uuid).all()