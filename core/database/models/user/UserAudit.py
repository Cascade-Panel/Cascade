""" The UserAudit model. """

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

class UserAudit(Base):
    """
        The UserAudit model.
        - A model to store the UserAudit information.

        Attributes:
            user_uuid (UUID): The UUID of the user.
            action (String): The action of the user.
            action_at (DateTime): The date the action was done.
            action_ip (Encrypted[String]): The IP of the user that did the action.
            success (Boolean): If the action was successful.
    """
    __tablename__ = 'UserAudit'

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_uuid = Column(UUIDType(binary=False), nullable=False)
    action = Column(String, nullable=False)
    action_at = Column(DateTime, nullable=False, default=datetime.datetime.now())

    action_ip = Column(EncryptedType(
        String, fetch_encryption_key(), AesEngine
    ), nullable=False)
    
    success = Column(Boolean, nullable=False, default=True)