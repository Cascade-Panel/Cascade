"""
This module provides the data-access-layer for managing User Audit records in the database.
"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.database.models.user.UserAudit import UserAudit
from core.database.DALs.base import BaseDAL
from datetime import datetime

class UserAuditDAL(BaseDAL):
    """
        Data Access Layer for managing User Audit records in the database.

        Args:
            db_session (Session): The database session.
    """
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
    
    async def new(self, user_audit: UserAudit) -> UserAudit:
        """
            Add a new User Audit record to the database.

            Args:
                user_audit (UserAudit): The User Audit record to add to the database.
            
            Returns:
                UserAudit: The User Audit record that was added to the database.
        """
        self.db_session.add(user_audit)
        self.db_session.commit()
        self.db_session.refresh(user_audit)
        return user_audit
    
    async def get(self, user_uuid: UUID, action_at: datetime) -> UserAudit | None:
        """
            Retrieve a User Audit record from the database by user UUID and action timestamp.

            Args:
                user_uuid (UUID): The UUID of the user.
                action_at (datetime): The timestamp of the action.
            
            Returns:
                UserAudit | None: The User Audit record with the specified user UUID and action timestamp, or None if not found.
        """
        return self.db_session.query(UserAudit).filter(
            UserAudit.user_uuid == user_uuid,
            UserAudit.action_at == action_at
        ).first()

    async def get_by_user(self, user_uuid: UUID) -> list[UserAudit]:
        """
            Retrieve all User Audit records for a specific user from the database.

            Args:
                user_uuid (UUID): The UUID of the user whose audit records to retrieve.
            
            Returns:
                list[UserAudit]: A list of User Audit records for the specified user.
        """
        return self.db_session.query(UserAudit).filter(UserAudit.user_uuid == user_uuid).all()

    async def update(self, user_audit: UserAudit) -> UserAudit:
        """
            Update a User Audit record in the database.

            Args:
                user_audit (UserAudit): The User Audit record to update in the database.
            
            Returns:
                UserAudit: The User Audit record that was updated in the database.
        """
        self.db_session.commit()
        self.db_session.refresh(user_audit)
        return user_audit
    
    async def refresh(self, user_audit: UserAudit) -> UserAudit:
        """
            Refresh an instance of a User Audit record object from the database.

            Args:
                user_audit (UserAudit): The User Audit record object to refresh.
            
            Returns:
                UserAudit: The User Audit record that was refreshed in the database.
        """
        self.db_session.refresh(user_audit)
        return user_audit

    async def delete(self, user_audit: UserAudit) -> UserAudit:
        """
            Delete a User Audit record from the database.

            Args:
                user_audit (UserAudit): The User Audit record to delete from the database.
            
            Returns:
                UserAudit: The User Audit record that was deleted from the database.
        """
        self.db_session.delete(user_audit)
        self.db_session.commit()
        return user_audit
    
    async def get_all(self) -> list[UserAudit]:
        """
            Retrieve all User Audit records from the database.

            Returns:
                list[UserAudit]: A list of all User Audit records in the database.
        """
        return self.db_session.query(UserAudit).all()
