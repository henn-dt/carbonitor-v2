# app/core/application/repositories/base/iread_repository.py
from abc import abstractmethod
from typing import Optional, List
from app.core.application.repositories.base.irepository import IRepository, T

class IReadRepository(IRepository[T]):
    """Base read repository interface"""
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        #it is similar to Union[T, None] if it finds the entity it returns T or else None
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass
    
    @abstractmethod
    def filter(self, **kwargs) -> List[T]:
        pass