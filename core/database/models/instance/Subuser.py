"""
    This module contains the Subuser model.
"""
import datetime
import uuid
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String
)
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine, EncryptedType
from core.database import Base, fetch_encryption_key


class Subuser(Base):
    """
        Represents a subuser in the Subusers table.

        Args:
            id (int): The ID of the subuser.
            uuid (UUID): The UUID of the subuser.
            server_uuid (UUID): The UUID of the server.
            added_at (DateTime): The date the subuser was added.
            last_accessed_at (DateTime): The date the subuser was last accessed.
            last_access_ip (String): The IP address of the last access.
            access_level (int): The access level of the subuser.
    """
    __tablename__ = "Subuser"

    id = Column(Integer, nullable=False, autoincrement=True)
    uuid = Column(UUIDType(binary=False), nullable=False, primary_key=True, default=uuid.uuid4())
    
    server_uuid = Column(UUIDType(binary=False), nullable=False)

    added_at = Column(EncryptedType(
        DateTime, fetch_encryption_key(), AesEngine
    ), nullable=False, default=datetime.datetime.now())
    last_accessed_at = Column(EncryptedType(
        DateTime, fetch_encryption_key(), AesEngine
    ), nullable=False, default=datetime.datetime.now())
    last_access_ip = Column(EncryptedType(
        String, fetch_encryption_key(), AesEngine
    ), nullable=False)

    access_level = Column(Integer, nullable=False, default=0)