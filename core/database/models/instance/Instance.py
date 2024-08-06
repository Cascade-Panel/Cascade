""" The Instance model. """

import datetime
import uuid
import pyotp
from sqlalchemy import Column, DateTime, String, Integer, Boolean
from sqlalchemy_utils import EncryptedType, StringEncryptedType, UUIDType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
from sqlalchemy.orm import relationship

from core.database import Base


def gen_uuid() -> uuid:
    return uuid.uuid4()

def fetch_code_expiry() -> datetime:
    return datetime.datetime.now() + datetime.timedelta(hours=2)

class Instance(Base):
    """
        The Instance model.
        - A model to store an instances information.

        Args:
            incus_uuid (UUID): The UUID of the instance.
            owner_uuid (UUID): The UUID of the owner.
            name (String): The name of the instance.
            chicken_uuid (UUID): The UUID of the chicken.
            node_uuid (UUID): The UUID of the node.
            description (String): The description of the instance.
            created_at (DateTime): The date the instance was created.
            updated_at (DateTime): The date the instance
    """

    __tablename__ = 'Instance'

    id = Column(Integer, primary_key=True, autoincrement=True)
    incus_uuid = Column(UUIDType(binary=False), nullable=False, default=gen_uuid())
    owner_uuid = Column(UUIDType(binary=False), nullable=False)
    name = Column(String, nullable=False, unique=True)
    chicken_uuid = Column(Integer, nullable=False)
    node_uuid = Column(Integer, nullable=False)

    subusers = relationship("Subuser", backref="server", primaryjoin="Server.incus_uuid == Subuser.server_uuid")

    description = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    updated_at = Column(DateTime, nullable=True)