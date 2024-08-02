"""
This module provides the data-access-layer for managing users in the database.
"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.database.models.user.User import User
from core.database.DALs.base import BaseDAL
from core.type_hints import Email

class UserDAL(BaseDAL):
    """
        Data Access Layer for managing users in the database.

        Attributes:
            db_session (Session): The database session.
    """
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
    
    async def new(self, user: User) -> User:
        """
            Add a new user to the database.

            Attributes:
                user (User): The user to add to the database.
            
            Returns:
                User: The user that was added to the database.
        """
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user
    
    async def get(self, uuid: UUID) -> User | None:
        """
            Retrieve a user from the database.

            Attributes:
                uuid (UUID): The UUID of the user to retrieve.
            
            Returns:
                User | None: The user with the specified UUID, or None if not found
        """
        return self.db_session.query(User).filter(User.uuid == uuid).first()
    
    async def get_by_email(self, email: Email) -> User | None:
        """
            Retrieve a user from the database by email.

            Attributes:
                email (Email): The email of the user to retrieve.
            
            Returns:
                User | Nonw: The user with the specified email, or None if not found.
        """
        return self.db_session.query(User).filter(User.email == email).first()

    async def update(self, user: User) -> User:
        """
            Update a user in the database.

            Attributes:
                user (User): The user to update in the database.
            
            Returns:
                User: The user that was updated in the database.
        """
        self.db_session.commit()
        self.db_session.refresh(user)
        return user
    
    async def refresh(self, user: User) -> User:
        """
            Refresh an instance of a user object from database.

            Attributes:
                user (User): The user object to refresh.
            
            Returns:
                User: The user that was refreshed in the database.
        """
        self.db_session.refresh(user)
        return user

    async def delete(self, user: User) -> User:
        """
            Delete a user from the database.

            Attributes:
                user (User): The user to delete from the database.
            
            Returns:
                User: The user that was deleted from the database.
        """
        self.db_session.delete(user)
        self.db_session.commit()
        return user
    
    async def get_all(self) -> list:
        """
            Retrieve all users from the database.

            Returns:
                list[User]: A list of all users in the database
        """
        return self.db_session.query(User).all()