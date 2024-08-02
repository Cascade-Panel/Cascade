"""
This module provides the data-access-layer for managing OAuth entries in the database.
"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.database.models.user.Oauth import Oauth
from core.database.DALs.base import BaseDAL

class OauthDAL(BaseDAL):
    """
        Data Access Layer for managing OAuth entries in the database.

        Attributes:
            db_session (Session): The database session.
    """
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
    
    async def new(self, oauth: Oauth) -> Oauth:
        """
            Add a new OAuth entry to the database.

            Attributes:
                oauth (Oauth): The OAuth entry to add to the database.
            
            Returns:
                Oauth: The OAuth entry that was added to the database.
        """
        self.db_session.add(oauth)
        self.db_session.commit()
        self.db_session.refresh(oauth)
        return oauth
    
    async def get(self, uuid: UUID) -> Oauth | None:
        """
            Retrieve an OAuth entry from the database.

            Attributes:
                uuid (UUID): The UUID of the OAuth entry to retrieve.
            
            Returns:
                Oauth | None: The OAuth entry with the specified UUID, or None if not found.
        """
        return self.db_session.query(Oauth).filter(Oauth.user_uuid == uuid).first()
    
    async def get_by_identifier(self, oauth_account_identifier: str) -> Oauth | None:
        """
            Retrieve an OAuth entry from the database by identifier.

            Attributes:
                oauth_account_identifier (str): The identifier of the OAuth entry to retrieve.
            
            Returns:
                Oauth | None: The OAuth entry with the specified identifier, or None if not found.
        """
        return self.db_session.query(Oauth).filter(Oauth.oauth_account_identifier == oauth_account_identifier).first()

    async def get_user_oauths(self, user_uuid: UUID) -> list[Oauth]:
        """
            Retrieve all OAuth entries for a user from the database.

            Attributes:
                user_uuid (UUID): The UUID of the user to retrieve OAuth entries for.
            
            Returns:
                list[Oauth]: A list of all OAuth entries for the specified user.
        """
        return self.db_session.query(Oauth).filter(Oauth.user_uuid == user_uuid).all()

    async def update(self, oauth: Oauth) -> Oauth:
        """
            Update an OAuth entry in the database.

            Attributes:
                oauth (Oauth): The OAuth entry to update in the database.
            
            Returns:
                Oauth: The OAuth entry that was updated in the database.
        """
        self.db_session.commit()
        self.db_session.refresh(oauth)
        return oauth
    
    async def refresh(self, oauth: Oauth) -> Oauth:
        """
            Refresh an instance of an OAuth entry object from the database.

            Attributes:
                oauth (Oauth): The OAuth entry object to refresh.
            
            Returns:
                Oauth: The OAuth entry that was refreshed in the database.
        """
        self.db_session.refresh(oauth)
        return oauth

    async def delete(self, oauth: Oauth) -> Oauth:
        """
            Delete an OAuth entry from the database.

            Attributes:
                oauth (Oauth): The OAuth entry to delete from the database.
            
            Returns:
                Oauth: The OAuth entry that was deleted from the database.
        """
        self.db_session.delete(oauth)
        self.db_session.commit()
        return oauth
    
    async def get_all(self) -> list[Oauth]:
        """
            Retrieve all OAuth entries from the database.

            Returns:
                list[Oauth]: A list of all OAuth entries in the database.
        """
        return self.db_session.query(Oauth).all()
