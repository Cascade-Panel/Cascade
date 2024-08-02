"""
This module provides the data-access-layer for managing MFA backup codes in the database.
"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.database.models.user.MfaBackupCodes import MfaBackupCodes
from core.database.DALs.base import BaseDAL

class MfaBackupCodesDAL(BaseDAL):
    """
        Data Access Layer for managing MFA backup codes in the database.

        Attributes:
            db_session (Session): The database session.
    """
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
    
    async def new(self, backup_code: MfaBackupCodes) -> MfaBackupCodes:
        """
            Add a new MFA backup code to the database.

            Attributes:
                backup_code (MfaBackupCodes): The MFA backup code to add to the database.
            
            Returns:
                MfaBackupCodes: The MFA backup code that was added to the database.
        """
        self.db_session.add(backup_code)
        self.db_session.commit()
        self.db_session.refresh(backup_code)
        return backup_code
    
    async def get(self, code: str) -> MfaBackupCodes | None:
        """
            Retrieve an MFA backup code from the database by its code.

            Attributes:
                code (str): The backup code to retrieve.
            
            Returns:
                MfaBackupCodes | None: The MFA backup code with the specified code, or None if not found.
        """
        return self.db_session.query(MfaBackupCodes).filter(MfaBackupCodes.code == code).first()

    async def get_by_user(self, user_uuid: UUID) -> list[MfaBackupCodes]:
        """
            Retrieve all MFA backup codes for a specific user from the database.

            Attributes:
                user_uuid (UUID): The UUID of the user to retrieve backup codes for.
            
            Returns:
                list[MfaBackupCodes]: A list of MFA backup codes for the specified user.
        """
        return self.db_session.query(MfaBackupCodes).filter(MfaBackupCodes.user_uuid == user_uuid).all()

    async def update(self, backup_code: MfaBackupCodes) -> MfaBackupCodes:
        """
            Update an MFA backup code in the database.

            Attributes:
                backup_code (MfaBackupCodes): The MFA backup code to update in the database.
            
            Returns:
                MfaBackupCodes: The MFA backup code that was updated in the database.
        """
        self.db_session.commit()
        self.db_session.refresh(backup_code)
        return backup_code
    
    async def refresh(self, backup_code: MfaBackupCodes) -> MfaBackupCodes:
        """
            Refresh an instance of an MFA backup code object from the database.

            Attributes:
                backup_code (MfaBackupCodes): The MFA backup code object to refresh.
            
            Returns:
                MfaBackupCodes: The MFA backup code that was refreshed in the database.
        """
        self.db_session.refresh(backup_code)
        return backup_code

    async def delete(self, backup_code: MfaBackupCodes) -> MfaBackupCodes:
        """
            Delete an MFA backup code from the database.

            Attributes:
                backup_code (MfaBackupCodes): The MFA backup code to delete from the database.
            
            Returns:
                MfaBackupCodes: The MFA backup code that was deleted from the database.
        """
        self.db_session.delete(backup_code)
        self.db_session.commit()
        return backup_code
    
    async def get_all(self) -> list[MfaBackupCodes]:
        """
            Retrieve all MFA backup codes from the database.

            Returns:
                list[MfaBackupCodes]: A list of all MFA backup codes in the database.
        """
        return self.db_session.query(MfaBackupCodes).all()
