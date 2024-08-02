"""
This module provides the data-access-layer for managing users in the database.
"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.database.models.user.User import User
from core.database.DALs.base import BaseDAL
from core.type_hints import Email

class UserDAL(BaseDAL):
    """Data Access Layer for managing users in the database."""
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    async def new(self, user: User):
        """Add a new user to the database."""
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user
    
    async def get(self, uuid: UUID) -> User:
        """Retrieve a user from the database."""
        return self.db_session.query(User).filter(User.uuid == uuid).first()
    
    async def get_by_email(self, email: Email) -> User:
        """Retrieve a user from the database by email."""
        return self.db_session.query(User).filter(User.email == email).first()
    
    async def update(self, user: User) -> User:
        """Update a user in the database."""
        self.db_session.commit()
        self.db_session.refresh(user)
        return user
    
    async def delete(self, user: User) -> User:
        """Delete a user from the database."""
        self.db_session.delete(user)
        self.db_session.commit()
        return user
    
    async def get_all(self) -> list:
        """Retrieve all users from the database."""
        return self.db_session.query(User).all()