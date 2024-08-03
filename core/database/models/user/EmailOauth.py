""" The EmailOauth model. """

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

class EmailOauth(Base):
    """
        The EmailOauth model.
        - A model to store the users email oauth login code and relevent information.

        Attributes:
            user_uuid (UUID): The UUID of the user.
            email (Encrypted[String]): The email of the user.
            code (Encrypted[UUID]): The email oauth code of the user.
            code_expiry (Encrypted[DateTime]): The expiry date of the email code.
            requested_on (Encrypted[DateTime]): The date the email was requested.
            has_been_used (Boolean): True if the email code has been used, False otherwise.
            used_on (Encrypted[DateTime]): The date the email code was used.
    """
    __tablename__ = 'EmailOauth'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_uuid = Column(UUIDType(binary=False), nullable=False)

    email = Column(EncryptedType(
        String, fetch_encryption_key(), AesEngine
    ), nullable=False, unique=True)

    code = Column(EncryptedType(
        UUIDType(binary=False), fetch_encryption_key(), AesEngine
    ), nullable=False, default=uuid.uuid4())

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