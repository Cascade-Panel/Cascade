""" The MfaBackupCodes model. """

import datetime
import uuid
import pyotp
from sqlalchemy import Column, DateTime, String, Integer, Boolean
from sqlalchemy_utils import EncryptedType, StringEncryptedType, UUIDType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from core.database import Base

def fetch_encryption_key() -> str:
    pass

def gen_uuid() -> uuid:
    return uuid.uuid4()

class MfaBackupCodes(Base):
    """
        The MfaBackupCodes model.

        Attributes:
            user_uuid (UUID): The UUID of the user.
            code (String): The backup code. Hashed.
            created_at (DateTime): The date the backup code

    """
    __tablename__ = 'MfaBackupCodes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_uuid = Column(UUIDType(binary=False), nullable=False) 
    code = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())