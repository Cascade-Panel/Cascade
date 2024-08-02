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

class Mfa(Base):
    """
        The Mfa model.
        - A model to store the Mfa information.

        Attributes:
    """
    __tablename__ = 'Mfa'

    user_uuid = Column(UUIDType(binary=False), nullable=False)

    is_setup = Column(Boolean, nullable=False, default=False)

    setup_at = Column(EncryptedType(
        DateTime, fetch_encryption_key(), AesEngine
    ), nullable=True)