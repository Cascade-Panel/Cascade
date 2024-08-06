"""
This module provides the data-access-layer for managing password resets in the database.
"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.database.models.user.PasswordReset import PasswordReset
from core.database.DALs.base import BaseDAL
from datetime import datetime

class PasswordResetDAL(BaseDAL):
    """
        Data Access Layer for managing password resets in the database.

        Args:
            db_session (Session): The database session.
    """
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
    
    async def new(self, password_reset: PasswordReset) -> PasswordReset:
        """
            Add a new password reset request to the database.

            Args:
                password_reset (PasswordReset): The password reset request to add to the database.
            
            Returns:
                PasswordReset: The password reset request that was added to the database.
        """
        self.db_session.add(password_reset)
        self.db_session.commit()
        self.db_session.refresh(password_reset)
        return password_reset
    
    async def get(self, uuid: UUID) -> PasswordReset | None:
        """
            Retrieve a password reset request from the database.

            Args:
                uuid (UUID): The UUID of the password reset request to retrieve.
            
            Returns:
                PasswordReset | None: The password reset request with the specified UUID, or None if not found.
        """
        return self.db_session.query(PasswordReset).filter(PasswordReset.user_uuid == uuid).first()
    
    async def get_by_code(self, reset_code: str) -> PasswordReset | None:
        """
            Retrieve a password reset request from the database by reset code.

            Args:
                reset_code (str): The reset code of the password reset request to retrieve.
            
            Returns:
                PasswordReset | None: The password reset request with the specified reset code, or None if not found.
        """
        return self.db_session.query(PasswordReset).filter(PasswordReset.reset_code == reset_code).first()
    
    async def get_all_expired(self) -> list[PasswordReset]:
        """
            Retrieve all expired password reset requests from the database.

            Returns:
                list[PasswordReset]: A list of all expired password reset requests in the database.
        """
        return self.db_session.query(PasswordReset).filter(PasswordReset.code_expiry < datetime.now()).all()

    async def update(self, password_reset: PasswordReset) -> PasswordReset:
        """
            Update a password reset request in the database.

            Args:
                password_reset (PasswordReset): The password reset request to update in the database.
            
            Returns:
                PasswordReset: The password reset request that was updated in the database.
        """
        self.db_session.commit()
        self.db_session.refresh(password_reset)
        return password_reset
    
    async def refresh(self, password_reset: PasswordReset) -> PasswordReset:
        """
            Refresh an instance of a password reset request object from the database.

            Args:
                password_reset (PasswordReset): The password reset request object to refresh.
            
            Returns:
                PasswordReset: The password reset request that was refreshed in the database.
        """
        self.db_session.refresh(password_reset)
        return password_reset

    async def delete(self, password_reset: PasswordReset) -> PasswordReset:
        """
            Delete a password reset request from the database.

            Args:
                password_reset (PasswordReset): The password reset request to delete from the database.
            
            Returns:
                PasswordReset: The password reset request that was deleted from the database.
        """
        self.db_session.delete(password_reset)
        self.db_session.commit()
        return password_reset
    
    async def get_all(self) -> list[PasswordReset]:
        """
            Retrieve all password reset requests from the database.

            Returns:
                list[PasswordReset]: A list of all password reset requests in the database.
        """
        return self.db_session.query(PasswordReset).all()
