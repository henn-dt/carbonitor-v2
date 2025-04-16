# app/core/application/repositories/base/iassociation_write_repository.py
from abc import abstractmethod
from typing import List, Optional, Dict, Any, Union

from sqlalchemy import BinaryExpression
from app.core.application.repositories.base.irepository import IRepository, T

class IAssociationWriteRepository(IRepository[T]):
    @abstractmethod
    def _build_key_condition(self, key_values: Dict[str, Any]) -> BinaryExpression:
        pass

    @abstractmethod
    def create_related(self, column: Union[str, List[str]], values: Union[Any, List[Dict[str, Any]]], base_values: Dict[str, Any]) -> List[T]:
        pass

    @abstractmethod
    def update_related(self, column: Union[str, List[str]], values: Union[Any, List[Dict[str, Any]]], filters: Dict[str, Any]) -> List[T]:
        pass

    @abstractmethod
    def delete_related(self, column: Union[str, List[str]], values: Union[Any, List[Any]], additional_filters: Optional[Dict[str, Any]] = None) -> int:
        pass