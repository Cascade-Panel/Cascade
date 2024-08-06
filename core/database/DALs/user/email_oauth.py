"""
This module provides the data-access-layer for managing Email OAuth records in the database.
"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.database.models.user.EmailOauth import EmailOauth
from core.database.DALs.base import BaseDAL
from core.type_hints import Email

class EmailOauthDAL(BaseDAL):
    """
        Data Access Layer for managing Email OAuth records in the database.

        Args:
            db_session (Session): The database session.
    """
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
    
    async def new(self, email_oauth: EmailOauth) -> EmailOauth:
        """
            Add a new Email OAuth record to the database.

            Args:
                email_oauth (EmailOauth): The Email OAuth record to add to the database.
            
            Returns:
                EmailOauth: The Email OAuth record that was added to the database.
        """
        self.db_session.add(email_oauth)
        self.db_session.commit()
        self.db_session.refresh(email_oauth)
        return email_oauth
    
    async def get_by_email(self, email: Email) -> EmailOauth | None:
        """
            Retrieve an Email OAuth record from the database by email.

            Args:
                email (str): The email to retrieve the Email OAuth record for.
            
            Returns:
                EmailOauth | None: The Email OAuth record with the specified email, or None if not found.
        """
        return self.db_session.query(EmailOauth).filter(EmailOauth.email == email).first()

    async def get_by_code(self, code: UUID) -> EmailOauth | None:
        """
            Retrieve an Email OAuth record from the database by OAuth code.

            Args:
                code (UUID): The OAuth code to retrieve the Email OAuth record for.
            
            Returns:
                EmailOauth | None: The Email OAuth record with the specified code, or None if not found.
        """
        return self.db_session.query(EmailOauth).filter(EmailOauth.code == code).first()

    async def update(self, email_oauth: EmailOauth) -> EmailOauth:
        """
            Update an Email OAuth record in the database.

            Args:
                email_oauth (EmailOauth): The Email OAuth record to update in the database.
            
            Returns:
                EmailOauth: The Email OAuth record that was updated in the database.
        """
        self.db_session.commit()
        self.db_session.refresh(email_oauth)
        return email_oauth
    
    async def refresh(self, email_oauth: EmailOauth) -> EmailOauth:
        """
            Refresh an instance of an Email OAuth record object from the database.

            Args:
                email_oauth (EmailOauth): The Email OAuth record object to refresh.
            
            Returns:
                EmailOauth: The Email OAuth record that was refreshed in the database.
        """
        self.db_session.refresh(email_oauth)
        return email_oauth

    async def delete(self, email_oauth: EmailOauth) -> EmailOauth:
        """
            Delete an Email OAuth record from the database.

            Args:
                email_oauth (EmailOauth): The Email OAuth record to delete from the database.
            
            Returns:
                EmailOauth: The Email OAuth record that was deleted from the database.
        """
        self.db_session.delete(email_oauth)
        self.db_session.commit()
        return email_oauth
    
    async def get_all(self) -> list[EmailOauth]:
        """
            Retrieve all Email OAuth records from the database.

            Returns:
                list[EmailOauth]: A list of all Email OAuth records in the database.
        """
        return self.db_session.query(EmailOauth).all()
