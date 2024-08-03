"""
This module provides the data-access-layer for managing Node records in the database.
"""

from uuid import UUID
from sqlalchemy.orm import Session
from core.database.models.instance.Node import Node
from core.database.DALs.base import BaseDAL

class NodeDAL(BaseDAL):
    """
    Data Access Layer for managing Node records in the database.

    Attributes:
        db_session (Session): The database session.
    """
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
    
    async def new(self, node: Node) -> Node:
        """
        Add a new Node record to the database.

        Attributes:
            node (Node): The Node record to add to the database.
        
        Returns:
            Node: The Node record that was added to the database.
        """
        self.db_session.add(node)
        self.db_session.commit()
        self.db_session.refresh(node)
        return node
    
    async def get_by_id(self, node_id: int) -> Node | None:
        """
        Retrieve a Node record from the database by its ID.

        Attributes:
            node_id (int): The ID of the Node record to retrieve.
        
        Returns:
            Node | None: The Node record with the specified ID, or None if not found.
        """
        return self.db_session.query(Node).filter(Node.id == node_id).first()

    async def get_by_uuid(self, node_uuid: UUID) -> Node | None:
        """
        Retrieve a Node record from the database by its UUID.

        Attributes:
            node_uuid (UUID): The UUID of the Node record to retrieve.
        
        Returns:
            Node | None: The Node record with the specified UUID, or None if not found.
        """
        return self.db_session.query(Node).filter(Node.uuid == node_uuid).first()

    async def update(self, node: Node) -> Node:
        """
        Update a Node record in the database.

        Attributes:
            node (Node): The Node record to update in the database.
        
        Returns:
            Node: The Node record that was updated in the database.
        """
        self.db_session.commit()
        self.db_session.refresh(node)
        return node
    
    async def refresh(self, node: Node) -> Node:
        """
        Refresh an instance of a Node record object from the database.

        Attributes:
            node (Node): The Node record object to refresh.
        
        Returns:
            Node: The Node record that was refreshed from the database.
        """
        self.db_session.refresh(node)
        return node

    async def delete(self, node: Node) -> Node:
        """
        Delete a Node record from the database.

        Attributes:
            node (Node): The Node record to delete from the database.
        
        Returns:
            Node: The Node record that was deleted from the database.
        """
        self.db_session.delete(node)
        self.db_session.commit()
        return node
    
    async def get_all(self) -> list[Node]:
        """
        Retrieve all Node records from the database.

        Returns:
            list[Node]: A list of all Node records in the database.
        """
        return self.db_session.query(Node).all()
