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

def fetch_code_expiry() -> datetime:
    return datetime.datetime.now() + datetime.timedelta(hours=2)

class PasswordReset(Base):
    """
        The PasswordReset model.
        - A model to store the PasswordReset information.

        Attributes:
    """
    __tablename__ = 'PasswordReset'

    user_uuid = Column(UUIDType(binary=False), nullable=False)

    reset_code = Column(EncryptedType(
        String, fetch_encryption_key(), AesEngine
    ), nullable=False, unique=True, default=gen_uuid())

    code_expiry = Column(EncryptedType(
        DateTime, fetch_encryption_key(), AesEngine
    ), nullable=False, default=fetch_code_expiry())

    requested_on = Column(EncryptedType(
        DateTime, fetch_encryption_key(), AesEngine
    ), nullable=False, default=datetime.datetime.now())

    has_been_used = Column(Boolean, nullable=False, default=False)

    used_on = Column(EncryptedType(
        DateTime, fetch_encryption_key(), AesEngine
    ), nullable=True)