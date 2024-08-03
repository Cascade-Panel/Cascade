""" The InstanceAudit model. """

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

class InstanceAudit(Base):
    """
        The InstanceAudit model.
        - A model to store the InstanceAudit information.

        Attributes:
            instance_uuid (UUID): The UUID of the instance.
            action (String): The action of the instance.
            action_at (DateTime): The date the action was done.
            action_user_uuid (UUID): The UUID of the user that did the action.
            action_user_ip (Encrypted[String]): The IP of the user that did the action.
            success (Boolean): If the action was successful.
    """
    __tablename__ = 'InstanceAudit'

    id = Column(Integer, primary_key=True, autoincrement=True)

    instance_uuid = Column(UUIDType(binary=False), nullable=False)
    action = Column(String, nullable=False)
    action_at = Column(DateTime, nullable=False, default=datetime.datetime.now())

    action_user_uuid = Column(UUIDType(binary=False), nullable=False)
    action_user_ip = Column(EncryptedType(
        String, fetch_encryption_key(), AesEngine
    ), nullable=False)
    
    success = Column(Boolean, nullable=False, default=True)