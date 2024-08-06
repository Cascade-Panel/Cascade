"""
This module provides the data-access-layer for managing Subuser records in the database.
"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.database.models.instance.Subuser import Subuser
from core.database.DALs.base import BaseDAL

class SubuserDAL(BaseDAL):
    """
    Data Access Layer for managing Subuser records in the database.

    Args:
        db_session (Session): The database session.
    """
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
    
    async def new(self, subuser: Subuser) -> Subuser:
        """
        Add a new Subuser record to the database.

        Args:
            subuser (Subuser): The Subuser record to add to the database.
        
        Returns:
            Subuser: The Subuser record that was added to the database.
        """
        self.db_session.add(subuser)
        self.db_session.commit()
        self.db_session.refresh(subuser)
        return subuser
    
    async def get_by_uuid(self, subuser_uuid: UUID) -> Subuser | None:
        """
        Retrieve a Subuser record from the database by its UUID.

        Args:
            subuser_uuid (UUID): The UUID of the Subuser record to retrieve.
        
        Returns:
            Subuser | None: The Subuser record with the specified UUID, or None if not found.
        """
        return self.db_session.query(Subuser).filter(Subuser.uuid == subuser_uuid).first()

    async def get_by_instance_id(self, instance_id: UUID) -> list[Subuser]:
        """
        Retrieve Subuser records from the database by instance ID (server_uuid).

        Args:
            instance_id (UUID): The instance ID (server_uuid) to retrieve Subuser records for.
        
        Returns:
            list[Subuser]: A list of Subuser records with the specified instance ID (server_uuid).
        """
        return self.db_session.query(Subuser).filter(Subuser.server_uuid == instance_id).all()

    async def update(self, subuser: Subuser) -> Subuser:
        """
        Update a Subuser record in the database.

        Args:
            subuser (Subuser): The Subuser record to update in the database.
        
        Returns:
            Subuser: The Subuser record that was updated in the database.
        """
        self.db_session.commit()
        self.db_session.refresh(subuser)
        return subuser
    
    async def refresh(self, subuser: Subuser) -> Subuser:
        """
        Refresh an instance of a Subuser record object from the database.

        Args:
            subuser (Subuser): The Subuser record object to refresh.
        
        Returns:
            Subuser: The Subuser record that was refreshed from the database.
        """
        self.db_session.refresh(subuser)
        return subuser

    async def delete(self, subuser: Subuser) -> Subuser:
        """
        Delete a Subuser record from the database.

        Args:
            subuser (Subuser): The Subuser record to delete from the database.
        
        Returns:
            Subuser: The Subuser record that was deleted from the database.
        """
        self.db_session.delete(subuser)
        self.db_session.commit()
        return subuser
    
    async def get_all(self) -> list[Subuser]:
        """
        Retrieve all Subuser records from the database.

        Returns:
            list[Subuser]: A list of all Subuser records in the database.
        """
        return self.db_session.query(Subuser).all()
