from abc import abstractmethod

from app.core.application.dtos.category.category_dto import (
    CategoryDTO,
    CategoryProperty,
    CategoryPropertySchema,
    CategoryResponseDTO,
    CategoryUpdateDTO,
)
from app.core.domain.entities.category import Category


class ICategoryMapper:

    @abstractmethod
    def create_entity_from_dto(CategoryDTO: CategoryDTO) -> Category:
        pass

    @abstractmethod
    def create_entity_from_update_dto(CategoryUpdateDTO: CategoryUpdateDTO) -> Category:
        pass

    @abstractmethod
    def create_dto_from_entity(Category: Category) -> CategoryResponseDTO:
        pass

    @abstractmethod
    def create_property_from_schema(
        property_id: int, property_schema=CategoryPropertySchema
    ) -> CategoryProperty:
        pass
