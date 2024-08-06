""" The Node model. """

import datetime
import uuid
import pyotp
from sqlalchemy import Column, DateTime, String, Integer, Boolean
from sqlalchemy_utils import EncryptedType, StringEncryptedType, UUIDType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from core.database import Base


def gen_uuid() -> uuid:
    return uuid.uuid4()

class Node(Base):
    """
        The Node model.
        - A model to store the Node information.

        Args:
            uuid (UUID): The UUID of the node.
            name (String): The name of the node.
            endpoint_url (String): The endpoint URL of the node.
            api_version (String): The API version of the node.
            created_at (DateTime): The date the node was created.
            updated_at (DateTime): The date the node was updated.
            created_by (UUID): The UUID of the user who created the node.
    """
    __tablename__ = 'Node'

    id = Column(Integer, primary_key=True, autoincrement=True)

    uuid = Column(UUIDType(binary=False), nullable=False, primary_key=True, default=uuid.uuid4())
    name = Column(String, nullable=False)
    endpoint_url = Column(String, nullable=False)
    api_version = Column(String, nullable=False, default="1.0")

    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now())

    created_by = Column(UUIDType(binary=False), nullable=False)