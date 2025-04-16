import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from datetime import datetime, date
from typing import List
from app.models.products import Product, ProductManager, ProductSerializer, oko_to_epdx, SourceType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

APP_DB_HOST = "mysql_dt.henn.com"
APP_DB_SCHEMA = "henn_carbonitor"
APP_DB_USER = "carbonitor"
APP_DB_PW = "henn"
APP_DB_PORT = 3306

epd_id = "8f11c179-e367-4833-93f3-10597923c79c" # concrete recycled generic c20/25
#epd_id = "b3fb0ba9-2376-49bf-b21a-7f7a5cd97233" #concrete c30/37
#epd_id = "8347f9a7-f4ec-4a36-a266-a0281f5fd16d" #average concrete c20/25
#epd_id = "d7bf4202-d1a8-4f3e-8861-c3d78cd2bf70" # windows double glazing
#epd_id = "f6861618-5a92-4c3a-94ba-9f7329b29662" # reinforcement steel wire

class TestProductManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up database connection"""
        try:
            # Database connection parameters
            DB_CONFIG = {
                'host': APP_DB_HOST,
                'database': APP_DB_SCHEMA,
                'user': APP_DB_USER,
                'password': APP_DB_PW,
                'port': APP_DB_PORT
            }
            
            # Create SQLAlchemy engine
            connection_string = (
                f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
                f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
            )
            cls.engine = create_engine(connection_string, echo=True)
            
            # Create session factory
            Session = sessionmaker(bind=cls.engine)
            cls.session = Session()
            
            logger.info("Database connection established successfully")
            
        except Exception as e:
            logger.error(f"Error setting up database connection: {str(e)}")
            raise

    @classmethod
    def tearDownClass(cls):
        """Clean up database connection"""
        cls.session.close()
        cls.engine.dispose()

    def test_list_all_products(self):
        """Test retrieving all products from database"""
        try:
            # Create ProductManager instance
            product_manager = ProductManager(self.session)
            
            # Get all products
            products = self.session.query(Product).all()
            
            # Log results
            logger.info(f"Found {len(products)} products in database")
            for product in products:
                logger.info(f"Product ID: {product.epd_id}, Name: {product.epd_name}")
            
            # Assert we can get products
            self.assertIsInstance(products, List)
            
        except Exception as e:
            logger.error(f"Error listing products: {str(e)}")
            raise

    def test_update_product(self):
        """Test updating an existing product with a specific ID"""
        try:
            product_manager = ProductManager(self.session)
            
            # Test data
            test_product_data = {
                'id': epd_id,
                "product_data" : oko_to_epdx(epd_id)[epd_id]
            }

            # First, check if product already exists
            existing_product = product_manager.get_product_by_epd_id(test_product_data['id'])
            
            if existing_product:
                logger.info(f"Product with ID {test_product_data['id']} already exists")
                # Compare existing product with test data
                updated_product = product_manager.check_and_update_product(test_product_data['product_data'], source = SourceType.OKOBAU)

                # Verify update
                self.assertIsNotNone(updated_product)
                self.assertEqual(updated_product.epd_id, test_product_data['id'])
            else:
                logger.info(f"Could not find product with ID: {test_product_data['id']} to update")
                

                
        except Exception as e:
            logger.error(f"Error checking and updating product: {str(e)}")
            raise


    def test_create_product(self):
        """Test creating a new product with a specific ID"""
        try:
            product_manager = ProductManager(self.session)
            
            # Test data
            test_product_data = {
                'id': epd_id,
                "product_data" : oko_to_epdx(epd_id)[epd_id]
            }



            # First, check if product already exists
            existing_product = product_manager.get_product_by_epd_id(test_product_data['id'])
            
            if existing_product:
                logger.info(f"Product with ID {test_product_data['id']} already exists")


            else:
                # Create new product
                new_product = product_manager.create_product(test_product_data['product_data'], source = SourceType.OKOBAU)
                logger.info(f"Created new product with ID: {new_product.epd_id}")
                
                # Verify creation
                created_product = product_manager.get_product_by_epd_id(test_product_data['id'])
                self.assertIsNotNone(created_product)
                self.assertEqual(created_product.epd_id, test_product_data['id'])
                
        except Exception as e:
            logger.error(f"Error creating product: {str(e)}")
            raise


    

def main():
    # Set up logging format
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    
    # Run tests
    unittest.main(verbosity=2)

if __name__ == '__main__':
    main()