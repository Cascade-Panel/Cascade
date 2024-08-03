""" The PasswordReset model."""

import datetime
import uuid
import pyotp
from sqlalchemy import Column, DateTime, String, Integer, Boolean
from sqlalchemy_utils import EncryptedType, StringEncryptedType, UUIDType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from core.database import Base, fetch_encryption_key


def gen_uuid() -> uuid:
    return uuid.uuid4()

def fetch_code_expiry() -> datetime:
    return datetime.datetime.now() + datetime.timedelta(hours=2)

class PasswordReset(Base):
    """
        The PasswordReset model.
        - A model to store the PasswordReset information.

        Attributes:
            user_uuid (UUID): The UUID of the user.
            reset_code (Encrypted[String]): The reset code.
            code_expiry (Encrypted[DateTime]): The expiry date of the reset code.
            requested_on (Encrypted[DateTime]): The date the reset code was requested.
            has_been_used (Boolean): True if the reset code has been used, False otherwise.
            used_on (Encrypted[DateTime]): The date the reset code was used.
    """
    __tablename__ = 'PasswordReset'

    id = Column(Integer, primary_key=True, autoincrement=True)
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