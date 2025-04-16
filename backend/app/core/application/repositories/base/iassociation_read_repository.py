# app/core/application/repositories/base/iassociation_read_repository.py
from abc import abstractmethod
from typing import Any, Dict, List, Optional, Union

from app.core.application.repositories.base.irepository import IRepository, T
from sqlalchemy import BinaryExpression


class IAssociationReadRepository(IRepository[T]):
    @abstractmethod
    def _build_key_condition(self, key_values: Dict[str, Any]) -> BinaryExpression:
        pass

    @abstractmethod
    def get_by_keys(self, keys: Dict[str, Any]) -> Optional[T]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        pass

    @abstractmethod
    def get_filtered(self, filters: Dict[str, Any]) -> List[T]:
        pass
    
    @abstractmethod
    def get_related_values(self, columns: Union[str, List[str]], filters: Dict[str, Any]) -> List[Union[Any, Dict[str, Any]]]:
        pass