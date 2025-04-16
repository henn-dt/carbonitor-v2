# backend/app/test/category/test_category_repository.py
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.core.domain.entities.category import Category
from app.infrastructure.container import Container


class TestCategoryRepository(unittest.TestCase):
    def setUp(self):
        self.container = Container()
        self.container.wire(modules=[__name__])
        self.test_category = Category(
            name="Test Category B",
            type="test_type",
            status="active",
            description="This is a test category",
            property_schema={"key": "value"}
        )
        self.write_repo = self.container.category_write_repository()
        self.read_repo = self.container.category_read_repository()

        # Cleanup from previous tests
        self._cleanup_test_data()
        
        # Created entities to track and clean up
        self.created_category = None

    def tearDown(self):
        # Clean up test data
        self._cleanup_test_data()

    def _cleanup_test_data(self):
        """Clean up any test data from previous test runs"""
        try:
            # Delete test category if it exists
            existing_category : Category = self.read_repo.get_by_name_and_type(self.test_category.name, self.test_category.type)
            if existing_category:
                self.write_repo.delete(existing_category.id)
        except Exception as e:
            print(f"Error during cleanup: {e}")

    def test_00_create(self):
        created_category= self.write_repo.create(self.test_category)
        self.created_category = created_category
        return print(created_category)

    def test_01_getall(self):
        return print(self.read_repo.get_all())
    
    def test_02_get_by_id(self):
        all_categories= self.read_repo.get_all()
        if all_categories: 
            category_id = all_categories[0].id
            print(f"trying to get category with id {category_id}")
            return print(self.read_repo.get_by_id(category_id))
    
    def test_03_get_by_name_and_type(self):
        return print(self.read_repo.get_by_name_and_type(self.test_category.name, self.test_category.type))

    def test_04_exist_by_name_and_type(self):
        return print(self.read_repo.exists_by_name_and_type(self.test_category.name, self.test_category.type))

    def test_05_get_by_properties(self):
        all_categories= self.read_repo.get_all()
        if all_categories:
            return print(self.read_repo.filter(type = "test_type"))

    def test_06_update_category(self):
        all_categories= self.read_repo.get_all()
        if all_categories:
            all_categories[0].description= str(all_categories[0].description)+" a"
            return print(self.write_repo.update(all_categories[0]))

    def test_07_delete_by_id(self):
        all_categories= self.read_repo.get_all()
        if not self.created_category and all_categories:
            print("no new category to delete, deleting newer category in the list")
            return print(self.write_repo.delete(all_categories[-1].id))

        deleted_category = self.write_repo.delete(self.created_category.id)
        if deleted_category:
            self.created_category = None
            return print(deleted_category)


if __name__ == '__main__':
    unittest.main()


