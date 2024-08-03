"""
This module provides the data-access-layer for managing InstanceAudit records in the database.
"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.database.models.instance.InstanceAudit import InstanceAudit
from core.database.DALs.base import BaseDAL

class InstanceAuditDAL(BaseDAL):
    """
    Data Access Layer for managing InstanceAudit records in the database.

    Attributes:
        db_session (Session): The database session.
    """
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
    
    async def new(self, instance_audit: InstanceAudit) -> InstanceAudit:
        """
        Add a new InstanceAudit record to the database.

        Attributes:
            instance_audit (InstanceAudit): The InstanceAudit record to add to the database.
        
        Returns:
            InstanceAudit: The InstanceAudit record that was added to the database.
        """
        self.db_session.add(instance_audit)
        self.db_session.commit()
        self.db_session.refresh(instance_audit)
        return instance_audit
    
    async def get_by_id(self, audit_id: int) -> InstanceAudit | None:
        """
        Retrieve an InstanceAudit record from the database by its ID.

        Attributes:
            audit_id (int): The ID of the InstanceAudit record to retrieve.
        
        Returns:
            InstanceAudit | None: The InstanceAudit record with the specified ID, or None if not found.
        """
        return self.db_session.query(InstanceAudit).filter(InstanceAudit.id == audit_id).first()

    async def get_all_by_instance_uuid(self, instance_uuid: UUID) -> list[InstanceAudit]:
        """
        Retrieve all InstanceAudit records from the database for a specific instance UUID.

        Attributes:
            instance_uuid (UUID): The UUID of the instance to retrieve audit records for.
        
        Returns:
            list[InstanceAudit]: A list of all InstanceAudit records for the specified instance UUID.
        """
        return self.db_session.query(InstanceAudit).filter(InstanceAudit.instance_uuid == instance_uuid).all()

    async def update(self, instance_audit: InstanceAudit) -> InstanceAudit:
        """
        Update an InstanceAudit record in the database.

        Attributes:
            instance_audit (InstanceAudit): The InstanceAudit record to update in the database.
        
        Returns:
            InstanceAudit: The InstanceAudit record that was updated in the database.
        """
        self.db_session.commit()
        self.db_session.refresh(instance_audit)
        return instance_audit
    
    async def refresh(self, instance_audit: InstanceAudit) -> InstanceAudit:
        """
        Refresh an instance of an InstanceAudit record object from the database.

        Attributes:
            instance_audit (InstanceAudit): The InstanceAudit record object to refresh.
        
        Returns:
            InstanceAudit: The InstanceAudit record that was refreshed from the database.
        """
        self.db_session.refresh(instance_audit)
        return instance_audit

    async def delete(self, instance_audit: InstanceAudit) -> InstanceAudit:
        """
        Delete an InstanceAudit record from the database.

        Attributes:
            instance_audit (InstanceAudit): The InstanceAudit record to delete from the database.
        
        Returns:
            InstanceAudit: The InstanceAudit record that was deleted from the database.
        """
        self.db_session.delete(instance_audit)
        self.db_session.commit()
        return instance_audit
    
    async def get_all(self) -> list[InstanceAudit]:
        """
        Retrieve all InstanceAudit records from the database.

        Returns:
            list[InstanceAudit]: A list of all InstanceAudit records in the database.
        """
        return self.db_session.query(InstanceAudit).all()
