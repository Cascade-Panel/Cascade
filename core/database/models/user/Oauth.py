""" The Oauth model. """

import datetime
import uuid
import pyotp
from sqlalchemy import Column, DateTime, String, Integer, Boolean
from sqlalchemy_utils import EncryptedType, StringEncryptedType, UUIDType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from core.database import Base, fetch_encryption_key


def gen_uuid() -> uuid:
    return uuid.uuid4()

class Oauth(Base):
    """
        The Oauth model.

        Args:
            user_uuid (UUID): The UUID of the user.
            oauth_type (String): The type of Oauth.
            oauth_account_identifier (Encrypted[String]): The identifier of the Oauth account.
            added_on (Encrypted[DateTime]): The date the Oauth was added.
            last_used (Encrypted[DateTime]): The date the Oauth
    """
    __tablename__ = 'Oauth'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_uuid = Column(UUIDType(binary=False), nullable=False) 
    oauth_type = Column(String, nullable=False)

    oauth_account_identifier = Column(EncryptedType(
        String, fetch_encryption_key(), AesEngine
    ), nullable=False, unique=True)

    added_on = Column(EncryptedType(
        DateTime, fetch_encryption_key(), AesEngine
    ), nullable=False, default=datetime.datetime.now())

    last_used = Column(EncryptedType(
        DateTime, fetch_encryption_key(), AesEngine
    ), nullable=False, default=datetime.datetime.now())