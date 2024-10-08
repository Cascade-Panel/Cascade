""" The Mfa model. """

import datetime
import uuid
import pyotp
from sqlalchemy import Column, DateTime, String, Integer, Boolean
from sqlalchemy_utils import EncryptedType, StringEncryptedType, UUIDType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from core.database import Base, fetch_encryption_key


def gen_uuid() -> uuid:
    return uuid.uuid4()

class Mfa(Base):
    """
        The Mfa model.
        - A model to store the Mfa information.

        Args:
            user_uuid (UUID): The UUID of the user.
            is_setting_up (Boolean): If the Mfa is setup.
            setup_at (Encrypted[DateTime]): The date the Mfa was setup.

    """
    __tablename__ = 'Mfa'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_uuid = Column(UUIDType(binary=False), nullable=False)

    is_setting_up = Column(Boolean, nullable=False, default=False)

    setup_at = Column(EncryptedType(
        DateTime, fetch_encryption_key(), AesEngine
    ), nullable=True)