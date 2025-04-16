# backend/app/test/category/test_category_repository.py
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.core.domain.entities.category import Category
from app.core.domain.entities.category_association import CategoryAssociation
from app.infrastructure.container import Container
from dependency_injector.wiring import Provide, inject


class TestCategoryAssociationRepository(unittest.TestCase):
    def setUp(self):
        self.container = Container()
        self.container.wire(modules=[__name__])
        self.write_repo = self.container.category_association_write_repository()
        self.read_repo = self.container.category_association_read_repository()
        self.category_write_repo = self.container.category_write_repository()
        self.created_category = None
        self.test_category = Category(
            name="Test Properties Association",
            type="product",
            status="active",
            description="Product properties for testing",
            property_schema={
                "color": {"type": "string", "enum": ["Red", "Blue", "Green"]},
                "size": {"type": "string", "enum": ["S", "M", "L", "XL"]},
                "price": {"type": "number"}
            }
        )
        # Setup entity details
        self.test_product_id = 999  # Test product ID - there´s no relationship to product through db structure so this can be whatever.
        self.entity_type = "product"  # Entity type

        # Values for the category association
        self.test_values = {
            "color": "Blue",
            "size": "M",
            "price": 29.99
        }
        # Cleanup from previous tests
        self._cleanup_test_data()
        
        # Created entities to track and clean up
        self.created_category = None
        self.created_association = None
    
#    def tearDown(self):
#        # Clean up test data
#        self._cleanup_test_data()
    
    def _cleanup_test_data(self):
        """Clean up any test data from previous test runs"""
        try:
            # Delete test category associations

            self.write_repo.delete_related(
                ["entity_id", "entity_type"],
                {"entity_id": self.test_product_id, "entity_type": self.entity_type}
            )
            
            # Delete test category if it exists
            category_write_repo = self.container.category_write_repository()
            category_read_repo = self.container.category_read_repository()

            existing_category : Category = category_read_repo.get_by_name_and_type(self.test_category.name, self.test_category.type)
            if existing_category:
                category_write_repo.delete(existing_category.id)
        except Exception as e:
            print(f"Error during cleanup: {e}")
    
    def _create_test_category(self) -> Category:
        """Helper to create a test category"""
        if self.created_category:
            return self.created_category
            
        self.created_category = self.category_write_repo.create(self.test_category)
        return self.created_category

    # ==== CREATE TESTS ==== 
    #   
    def test_00_create_association(self):

        db_context = self.container.db_context()
        """Test creating a category association"""
        # First create a category

        created_category : Category = self.category_write_repo.create(self.test_category)
        print(f"created test category: {created_category}")

        # Make sure we have the ID - debugging step
        if created_category.id is None:
            # Try to retrieve the saved category to get its ID
            with db_context.session() as session:
                refreshed_category = session.query(Category).filter_by(name=self.test_category.name).first()
                if refreshed_category:
                    created_category.id = refreshed_category.id
                    print(f"Retrieved category ID: {created_category.id}")
                else:
                    print("Category was not found in database after creation!")
        
        # Create association
        association = CategoryAssociation(
            category_id = int(created_category.id),
            entity_id=self.test_product_id,
            entity_type=self.entity_type,
            values=self.test_values
        )


        print(f"association: {association}")

        base_values = {
            "category_id": association.category_id,
            "entity_type": association.entity_type,
            "values": association.values
        }
        print(f"Base values: {base_values}")
        
        created = self.write_repo.create_related(column="entity_id", values=self.test_product_id , base_values = base_values)
        print(f"created {len(created)} associations")
        self.created_association : CategoryAssociation = created[0]

        with db_context.session() as session:
            session.flush()

        verified_association = self.read_repo.get_by_keys({"id" : self.created_association.id, 
                                                            "entity_type" : self.created_association.entity_type,
                                                            "entity_id" : self.created_association.entity_id,
                                                            "category_id" : self.created_association.category_id,})

        # check created association:
        print(f"created association: {verified_association}")

        # need to cleanup category here
        self.category_write_repo.delete(created_category.id)

        # Assert
        self.assertIsNotNone(created)
        self.assertEqual(1, len(created))
        self.assertEqual(created_category.id, self.created_association.category_id)
        self.assertEqual(self.test_product_id, self.created_association.entity_id)
        self.assertEqual(self.test_values, self.created_association.values)


    def test_01_associate_entity_with_category(self):
        """Test associate_entity_with_category method"""
        # First create a category
        category = self._create_test_category()
        
        # Associate product with category
        association = self.write_repo.associate_entity_with_category(
            entity_id = self.test_product_id,
            entity_type= self.entity_type,
            category_id= category.id,
            values=self.test_values
        )
        self.created_association = association
        
        # Assert
        self.assertIsNotNone(association)
        self.assertEqual(category.id, association.category_id)
        self.assertEqual(self.test_product_id, association.entity_id)
        self.assertEqual(self.entity_type, association.entity_type)
        self.assertEqual(self.test_values, association.values)
    
     
    def test_02_batch_associate_entity_with_categories(self):
        #Test batch associating an entity with multiple categories
        # Create two test categories
        category1 = self._create_test_category()
        
        # Create a second category
        category2 = self.category_write_repo.create(Category(
            name="Second Test Category",
            type="product",
            status="active",
            description="Another test category",
            property_schema={"feature": {"type": "boolean"}}
        ))
        
        # Batch associate
        category_data = [
            {"category_id": category1.id, "values": self.test_values},
            {"category_id": category2.id, "values": {"feature": True}}
        ]
        
        associations = self.write_repo.batch_associate_entity_with_categories(
            self.test_product_id,
            self.entity_type,
            category_data
        )


        
        # Assert
        self.assertEqual(2, len(associations))
        self.assertEqual(category1.id, associations[0].category_id)
        self.assertEqual(category2.id, associations[1].category_id)
        self.assertEqual(self.test_values, associations[0].values)
        self.assertEqual({"feature": True}, associations[1].values)
        
        # Clean up the second category
        self.category_write_repo.delete(category2.id)

        # need to cleanup category 1 too
        self.category_write_repo.delete(category1.id)

    # ==== READ TESTS ====
    
    def test_03_get_by_keys(self):
        """Test get_by_keys method"""
        # Create test data
        category = self._create_test_category()
        association = self.write_repo.associate_entity_with_category(
            self.test_product_id,
            self.entity_type,
            category.id,
            self.test_values
        )
        self.created_association = association
        
        # Get by keys
        found = self.read_repo.get_by_keys({
            "category_id": category.id,
            "entity_id": self.test_product_id,
            "entity_type": self.entity_type
        })
        
        # Assert
        self.assertIsNotNone(found)
        self.assertEqual(category.id, found.category_id)
        self.assertEqual(self.test_product_id, found.entity_id)
        self.assertEqual(self.test_values, found.values)
    

    def test_04_get_filtered(self):
        """Test get_filtered method"""
        # Create test data
        category = self._create_test_category()
        association = self.write_repo.associate_entity_with_category(
            self.test_product_id,
            self.entity_type,
            category.id,
            self.test_values
        )
        self.created_association = association
        
        # Get filtered by entity_id
        found = self.read_repo.get_filtered({
            "entity_id": self.test_product_id
        })
        
        # Assert
        self.assertEqual(1, len(found))
        self.assertEqual(category.id, found[0].category_id)
        
        # Get filtered by entity_type
        found = self.read_repo.get_filtered({
            "entity_type": self.entity_type
        })
        
        # Assert at least one result (there might be other entities)
        self.assertGreaterEqual(len(found), 1)
        
        # Find our specific association
        our_association = next((a for a in found if a.entity_id == self.test_product_id), None)
        self.assertIsNotNone(our_association)
    

    def test_05_get_related_values(self):
        """Test get_related_values method"""
        # Create test data
        category = self._create_test_category()
        association = self.write_repo.associate_entity_with_category(
            self.test_product_id,
            self.entity_type,
            category.id,
            self.test_values
        )
        self.created_association = association
        
        # Get related values - single column
        entity_ids = self.read_repo.get_related_values(
            "entity_id",
            {"category_id": category.id}
        )

        print(f"entity_ids : {entity_ids}")
        
        # Assert
        self.assertIn(self.test_product_id, entity_ids)
        
        # Get related values - multiple columns
        results = self.read_repo.get_related_values(
            ["entity_id", "entity_type"],
            {"category_id": category.id}
        )
        
        print(f"results : {results}")
        # Assert
        found = False
        for result in results:
            if result["entity_id"] == self.test_product_id and result["entity_type"] == self.entity_type:
                found = True
                break
        self.assertTrue(found)
    

    def test_06_get_category_properties_for_product(self):
        """Test get_category_properties_for_product method"""
        # Create test data
        category = self._create_test_category()
        association = self.write_repo.associate_entity_with_category(
            self.test_product_id,
            self.entity_type,
            category.id,
            self.test_values
        )
        self.created_association = association
        
        # Get properties
        properties = self.read_repo.get_category_properties_for_entity(self.test_product_id)

        print(f"product properties: {properties}")
        
        # Assert
        self.assertGreaterEqual(len(properties), 1)
        
        # Find our category
        our_category = next((p for p in properties if p["category_id"] == category.id), None)
        self.assertIsNotNone(our_category)
        self.assertEqual(category.name, our_category["category_name"])
        self.assertEqual(category.property_schema, our_category["property_schema"])
        self.assertEqual(self.test_values, our_category["values"])
    

    def test_07_get_by_entity(self):
        """Test get_by_entity method"""
        # Create test data
        category = self._create_test_category()
        association = self.write_repo.associate_entity_with_category(
            self.test_product_id,
            self.entity_type,
            category.id,
            self.test_values
        )
        self.created_association = association
        
        # Get by entity
        associations = self.read_repo.get_by_entity(
            self.entity_type,
            self.test_product_id
        )
        
        # Assert
        self.assertGreaterEqual(len(associations), 1)
        
        # Find our association
        our_association = next((a for a in associations if a.category_id == category.id), None)
        self.assertIsNotNone(our_association)
        self.assertEqual(self.test_values, our_association.values)

    
    # ==== UPDATE TESTS ====
    

    def test_08_update_related(self):
        """Test update_related method"""
        # Create test data
        category = self._create_test_category()
        association = self.write_repo.associate_entity_with_category(
            self.test_product_id,
            self.entity_type,
            category.id,
            self.test_values
        )
        self.created_association = association
        
        # Update the values
        updated_values = {
            "color": "Green",
            "size": "L",
            "price": 39.99
        }
        
        updated = self.write_repo.update_related(
            "values",
            updated_values,
            {
                "category_id": category.id,
                "entity_id": self.test_product_id,
                "entity_type": self.entity_type
            }
        )
        
        # Assert
        self.assertEqual(1, len(updated))
        self.assertEqual(updated_values, updated[0].values)
        
        # Verify the update persisted
        found = self.read_repo.get_by_keys({
            "category_id": category.id,
            "entity_id": self.test_product_id,
            "entity_type": self.entity_type
        })
        
        self.assertEqual(updated_values, found.values)


    def test_09_update_entity_category_values(self):
        """Test update_entity_category_values method"""
        # Create test data
        category = self._create_test_category()
        association = self.write_repo.associate_entity_with_category(
            self.test_product_id,
            self.entity_type,
            category.id,
            self.test_values
        )
        self.created_association = association
        
        # Update values
        updated_values = {
            "color": "Red",
            "size": "XL",
            "price": 49.99
        }
        
        updated = self.write_repo.update_entity_category_values(
            self.test_product_id,
            self.entity_type,
            category.id,
            updated_values
        )
        
        # Assert
        self.assertIsNotNone(updated)
        self.assertEqual(updated_values, updated.values)
        
        # Verify the update persisted
        found = self.read_repo.get_by_keys({
            "category_id": category.id,
            "entity_id": self.test_product_id,
            "entity_type": self.entity_type
        })
        
        self.assertEqual(updated_values, found.values)

 
if __name__ == '__main__':
    unittest.main()


