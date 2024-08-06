""" This module contains the Chicken model. """
import datetime
import uuid
from sqlalchemy import (
    Column,
    Integer,
    String,
    Uuid,
    DateTime,
    Boolean,
)

from core.database import Base


class Chicken(Base):
    """
        The Chicken model.
        - A model to store the Chicken information.

        Args:
            identifier (Integer): The identifier of the Chicken.
            uuid (Uuid): The UUID of the Chicken.
            name (String): The name of the Chicken.
            type (String): The type of the Chicken.
            endpoint_url (String): The endpoint URL of the Chicken.
            suspended (Boolean): True if the Chicken is suspended, False otherwise.
            raw_yml (String): The raw YML string of the Chicken.
    """
    __tablename__ = "Chicken"

    id = Column(Integer, nullable=False, autoincrement=True)
    uuid = Column(Uuid, nullable=False, primary_key=True, default=uuid.uuid4())
    name = Column(String, nullable=False)
    
    ## make a columnm called type that can only be one of the following values: OCI, SYSTEM, or VM
    type = Column(String, nullable=False)
    
    endpoint_url = Column(String, nullable=False)

    ## column to show if the chicken is suspended or not
    suspended = Column(Boolean, nullable=False, default=False)

    added_on = Column(DateTime, nullable=False, default=datetime.datetime.now())

    ## column to store the YML string of the Chicken
    raw_yml = Column(String, nullable=False)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'chicken'
    }

    @staticmethod
    def validate_type(type_value):
        if type_value not in ['OCI', 'SYSTEM', 'VM']:
            raise ValueError('Invalid type')

    @staticmethod
    def before_insert(mapper, connection, target):
        Chicken.validate_type(target.type)

    @staticmethod
    def before_update(mapper, connection, target):
        Chicken.validate_type(target.type)