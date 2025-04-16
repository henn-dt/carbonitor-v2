# app/core/application/repositories/base/iwrite_repository.py
from abc import abstractmethod
from typing import Generic, TypeVar
from app.core.application.repositories.base.irepository import IRepository

T = TypeVar('T')

class IWriteRepository(IRepository[T], Generic[T]):
    """Base write repository interface for single entity operations"""
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """Create a new entity"""
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        """Update an existing entity"""
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        """Delete an entity by id"""
        pass