"""
This module provides the data-access-layer for managing MFA (Multi-Factor Authentication) records in the database.
"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.database.models.user.Mfa import Mfa
from core.database.DALs.base import BaseDAL

class MfaDAL(BaseDAL):
    """
        Data Access Layer for managing MFA records in the database.

        Args:
            db_session (Session): The database session.
    """
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
    
    async def new(self, mfa: Mfa) -> Mfa:
        """
            Add a new MFA record to the database.

            Args:
                mfa (Mfa): The MFA record to add to the database.
            
            Returns:
                Mfa: The MFA record that was added to the database.
        """
        self.db_session.add(mfa)
        self.db_session.commit()
        self.db_session.refresh(mfa)
        return mfa
    
    async def get(self, user_uuid: UUID) -> Mfa | None:
        """
            Retrieve an MFA record from the database by user UUID.

            Args:
                user_uuid (UUID): The UUID of the user whose MFA record to retrieve.
            
            Returns:
                Mfa | None: The MFA record for the specified user, or None if not found.
        """
        return self.db_session.query(Mfa).filter(Mfa.user_uuid == user_uuid).first()

    async def update(self, mfa: Mfa) -> Mfa:
        """
            Update an MFA record in the database.

            Args:
                mfa (Mfa): The MFA record to update in the database.
            
            Returns:
                Mfa: The MFA record that was updated in the database.
        """
        self.db_session.commit()
        self.db_session.refresh(mfa)
        return mfa
    
    async def refresh(self, mfa: Mfa) -> Mfa:
        """
            Refresh an instance of an MFA record object from the database.

            Args:
                mfa (Mfa): The MFA record object to refresh.
            
            Returns:
                Mfa: The MFA record that was refreshed in the database.
        """
        self.db_session.refresh(mfa)
        return mfa

    async def delete(self, mfa: Mfa) -> Mfa:
        """
            Delete an MFA record from the database.

            Args:
                mfa (Mfa): The MFA record to delete from the database.
            
            Returns:
                Mfa: The MFA record that was deleted from the database.
        """
        self.db_session.delete(mfa)
        self.db_session.commit()
        return mfa
    
    async def get_all(self) -> list[Mfa]:
        """
            Retrieve all MFA records from the database.

            Returns:
                list[Mfa]: A list of all MFA records in the database.
        """
        return self.db_session.query(Mfa).all()