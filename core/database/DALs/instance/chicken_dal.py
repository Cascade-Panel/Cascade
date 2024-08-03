"""
This module provides the data-access-layer for managing Chicken records in the database.
"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.database.models.instance.Chicken import Chicken
from core.database.DALs.base import BaseDAL

class ChickenDAL(BaseDAL):
    """
    Data Access Layer for managing Chicken records in the database.

    Attributes:
        db_session (Session): The database session.
    """
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
    
    async def new(self, chicken: Chicken) -> Chicken:
        """
        Add a new Chicken record to the database.

        Attributes:
            chicken (Chicken): The Chicken record to add to the database.
        
        Returns:
            Chicken: The Chicken record that was added to the database.
        """
        self.db_session.add(chicken)
        self.db_session.commit()
        self.db_session.refresh(chicken)
        return chicken
    
    async def get_by_uuid(self, uuid: UUID) -> Chicken | None:
        """
        Retrieve a Chicken record from the database by UUID.

        Attributes:
            uuid (UUID): The UUID to retrieve the Chicken record for.
        
        Returns:
            Chicken | None: The Chicken record with the specified UUID, or None if not found.
        """
        return self.db_session.query(Chicken).filter(Chicken.uuid == uuid).first()

    async def get_by_name(self, name: str) -> Chicken | None:
        """
        Retrieve a Chicken record from the database by name.

        Attributes:
            name (str): The name to retrieve the Chicken record for.
        
        Returns:
            Chicken | None: The Chicken record with the specified name, or None if not found.
        """
        return self.db_session.query(Chicken).filter(Chicken.name == name).first()

    async def update(self, chicken: Chicken) -> Chicken:
        """
        Update a Chicken record in the database.

        Attributes:
            chicken (Chicken): The Chicken record to update in the database.
        
        Returns:
            Chicken: The Chicken record that was updated in the database.
        """
        self.db_session.commit()
        self.db_session.refresh(chicken)
        return chicken
    
    async def refresh(self, chicken: Chicken) -> Chicken:
        """
        Refresh an instance of a Chicken record object from the database.

        Attributes:
            chicken (Chicken): The Chicken record object to refresh.
        
        Returns:
            Chicken: The Chicken record that was refreshed in the database.
        """
        self.db_session.refresh(chicken)
        return chicken

    async def delete(self, chicken: Chicken) -> Chicken:
        """
        Delete a Chicken record from the database.

        Attributes:
            chicken (Chicken): The Chicken record to delete from the database.
        
        Returns:
            Chicken: The Chicken record that was deleted from the database.
        """
        self.db_session.delete(chicken)
        self.db_session.commit()
        return chicken
    
    async def get_all(self) -> list[Chicken]:
        """
        Retrieve all Chicken records from the database.

        Returns:
            list[Chicken]: A list of all Chicken records in the database.
        """
        return self.db_session.query(Chicken).all()
