

from app.core.application.dtos.category_association.category_association_dto import (CategoryAssociationCategoryDTO, CategoryAssociationDTO, CategoryAssociationResponseDTO)
from app.core.application.mappers.icategory_association_mapper import ICategoryAssociationMapper
from app.core.domain.entities.category_association import CategoryAssociation


class CategoryAssociationMapper(ICategoryAssociationMapper):

    @staticmethod
    def create_entity_from_association_dto(association_dto : CategoryAssociationDTO) -> CategoryAssociation:
        return CategoryAssociation(**association_dto.model_dump(exclude_unset=True))

    @staticmethod
    def create_dto_from_association_entity(association_entity : CategoryAssociation) -> CategoryAssociationResponseDTO :
        try:
            # Get the category data as dict
            association_data = association_entity.to_dict() 
            response_dto = CategoryAssociationResponseDTO(**association_data)
            return response_dto        
        except Exception as e:
            print(f"Error creating Category Association Response object: {str(e)}")

    @staticmethod
    def category_dto_from_association_entity(association_entity: CategoryAssociation) -> CategoryAssociationCategoryDTO:
        try:
            association_data = association_entity.to_dict() 
            response_dto = CategoryAssociationCategoryDTO(**association_data)
            return response_dto
        except Exception as e:
            print(f"Error creating Category Response object: {str(e)}")

    
