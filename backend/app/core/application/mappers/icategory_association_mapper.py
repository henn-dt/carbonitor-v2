from abc import abstractmethod
from typing import TypeVar

from app.core.application.dtos.category_association.category_association_dto import (
    CategoryAssociationCategoryDTO, CategoryAssociationDTO, CategoryAssociationResponseDTO)
from app.core.domain.entities.category_association import CategoryAssociation


class ICategoryAssociationMapper:

    @abstractmethod
    def create_entity_from_association_dto(entity_dto : CategoryAssociationDTO) -> CategoryAssociation:
        pass

    @abstractmethod
    def create_dto_from_association_entity(entity : CategoryAssociation) -> CategoryAssociationResponseDTO :
        pass

    @abstractmethod
    def category_dto_from_association_entity(entity: CategoryAssociation) -> CategoryAssociationCategoryDTO:
        pass