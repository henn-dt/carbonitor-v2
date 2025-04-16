import json
from pathlib import Path
from datetime import datetime
import requests
import lcax
from enum import Enum

from .base import AppBase as Base, TimestampMixin, DatabaseType

from sqlalchemy import Column, Integer, String, Date, Float, Text, DateTime, create_engine
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
SQLALCHEMY_BIND = DatabaseType.CARBONITOR_DATA.value

import logging
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# product Model, to replace through alembic later
class Product(TimestampMixin, Base):
    __tablename__ = 'products'
    __table_args__ = {'schema': SQLALCHEMY_BIND}

    id = Column(Integer, primary_key=True)
    status = Column(String(50), nullable=False, default='active')
    
    # EPD specific fields
    epd_sourceName = Column(String(255), nullable=False)
    epd_sourceUrl = Column(String(500))
    epd_id = Column(String(100), unique=True)
    epd_name = Column(String(255), nullable=False)
    epd_version = Column(String(50))
    epd_publishedDate = Column(Date)
    epd_validUntil = Column(Date)
    epd_standard = Column(String(100))
    epd_subtype = Column(String(100))
    epd_comment = Column(Text)
    epd_location = Column(String(100))
    epd_formatVersion = Column(String(100))
    
    # Physical conversion properties
    epd_declaredUnit = Column(String(50), nullable=False)
    epd_gross_density = Column(Float)
    epd_bulk_density = Column(Float)
    epd_grammage = Column(Float)
    epd_linear_density = Column(Float)
    epd_layer_thickness = Column(Float)
    
    # JSON data
    epdx = Column(MutableDict.as_mutable(JSON))


class SourceType(Enum):
    OKOBAU = "Oekobaudat"
    CUSTOM = "Custom"

# Serializer class to handle EPDX conversion

class ProductSerializer:
    @staticmethod
    def from_epdx(epdx_data, source = SourceType.CUSTOM):
        """Convert epdx data to Product object"""
        
        def find_conversions(_epdx_data):
            conversions = _epdx_data.get('conversions')
            if conversions == None:
                return False
            output = {}
            for conversion in conversions:
                conversion_data = json.loads(conversion['metaData'])
                name = conversion_data['name'].replace(" ", "_")
                field_name = "epd_"+name
                value = conversion_data['value']
                output.update({field_name : value})
            return output
        
        _epdx_data = json.loads(epdx_data)

        product_data = {
            ''
            'epdx' : _epdx_data, 
            'epd_name': _epdx_data.get('name'),
            'epd_id': _epdx_data.get('id'),
            'epd_standard': _epdx_data.get('standard'),  # Field name conversion
            'epd_validUntil': datetime.strptime(_epdx_data.get('validUntil'), '%Y-%m-%d').date() if _epdx_data.get('valid_until') else None,
            'epd_publishedDate': datetime.strptime(_epdx_data.get('publishedDate'), '%Y-%m-%d').date()if _epdx_data.get('published_date') else None,
            'epd_subtype': _epdx_data.get('subtype'),
            'epd_declaredUnit': _epdx_data.get('declaredUnit'),
            'epd_location': _epdx_data.get('location'),
            'epd_version': _epdx_data.get('version'),
            'epd_formatVersion': _epdx_data.get('formatVersion'),

        }
         
        conversions = find_conversions(_epdx_data)
        if conversions:
            product_data.update(conversions)
        
                
        match source:
            case SourceType.OKOBAU:
                product_data.update({'epd_sourceName' : SourceType.OKOBAU.value, 'epd_sourceUrl' : f"{OKOBAU_URL}/processes/{_epdx_data.get('id')}"})
            case _:
                product_data.update({'epd_sourceName' : "custom"})

        return product_data
    
    @staticmethod
    def to_epdx(product):
        return product.epdx
    
# CRUD product operations

class ProductManager:
    def __init__(self, session):
        self.session = session

    
    def create_product(self, epdx_data, source = SourceType.CUSTOM):
        """Create a new product from JSON data"""
        try:
            product_data = ProductSerializer.from_epdx(epdx_data, source)
            product = Product(**product_data)
            self.session.add(product)
            self.session.commit()
            return product
        except Exception as e:
            self.session.rollback()
            raise e

    def get_product_by_epd_id(self, epd_id):
        """Retrieve a product by its epd ID"""
        return self.session.query(Product).filter_by(epd_id=epd_id).first()
    
    def update_product(self, epdx_data, source = SourceType.CUSTOM):
        """Update an existing product"""
        epd_id = json.loads(epdx_data)["id"]
        try:
            product = self.get_product_by_epd_id(epd_id)
            if not product:
                raise ValueError(f"Product with epd_id {epd_id} not found")
            
            product_data = ProductSerializer.from_epdx(epdx_data, source)
            for key, value in product_data.items():
                setattr(product, key, value)
            
            self.session.commit()
            return product
        except Exception as e:
            self.session.rollback()
            raise e

    def delete_product(self, epd_id):
        """Delete a product"""
        try:
            product = self.get_product_by_epd_id(epd_id)
            if not product:
                raise ValueError(f"Product with epd_id {epd_id} not found")
            
            self.session.delete(product)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        
    def product_exists(self, epd_id):
        """Check if product exists"""
        existing_product = self.get_product_by_epd_id(epd_id)
        
        if not existing_product:
            return False
        return True

    def check_product(self, epdx_data):
        """Check if product exists and matches epdx"""
        _epdx_data = json.loads(epdx_data)
        if not self.product_exists(_epdx_data.get('id')):
            return False
        existing_data = ProductSerializer.to_epdx(self.get_product_by_epd_id(_epdx_data.get('id')))

        if existing_data != epdx_data:
            return False
        return True
    
    def check_and_update_product(self, epdx_data, source=SourceType.CUSTOM):
        """Check if product exists and update if necessary"""
        _epdx_data = json.loads(epdx_data)
        epd_id = _epdx_data.get('id')
        if not self.product_exists(epd_id):
            return self.create_product(epdx_data, source)
        if not self.check_product(epdx_data):
            return self.update_product(epdx_data, source)
        return self.get_product_by_epd_id(epd_id)




###############################
#OKOBAU

OKOBAU_URL = "https://oekobaudat.de/OEKOBAU.DAT/resource/datastocks/ca70a7e6-0ea4-4e90-a947-d44585783626"

def oko_get_epds(limit=-1) -> dict:
    """Get EPDs from Ökobau - defaults to A2 Datasets"""

    if limit > 0:
        response = requests.get(f"{OKOBAU_URL}/processes?search=true&compliance=c0016b33-8cf7-415c-ac6e-deba0d21440d&format=json&pageSize={limit}")
    else:
        response = requests.get(f"{OKOBAU_URL}/processes?search=true&compliance=c0016b33-8cf7-415c-ac6e-deba0d21440d&format=json")
    response.raise_for_status()
    data = response.json()

    print(f"Retrieved {data.get('pageSize')} EPDs out of {data.get('totalCount')} from Ökobau")

    return data

def oko_get_full_epd(uid: str) -> dict:
    """Get the full dataset for a single EPD"""

    base_url = f"{OKOBAU_URL}/processes/{uid}"
    response = requests.get(f"{base_url}?format=json&view=extended")

    response.raise_for_status()
    data = response.json()
    data["source"] = base_url

    return data

def oko_get_full_epd_str(uid: str) -> str:
    """Get the full dataset for a single EPD and return it as a string"""
    return json.dumps(oko_get_full_epd(uid))

def oko_to_epdx(uid: str):
    """query Okobau for an epd with a given id, and converts it to 
    epdx in json format
    returns a dictionary where key = epd_id : value = epdx json string
    """
    output = "no id provided - this method needs the ID of an epd from Okobau"
    if uid == None:
        return output

    epd_id = []

    if isinstance(uid, list):
        epd_id = uid
    else:
        epd_id = [uid]

    for id in epd_id:
        try:
            #gets the full epd data in ilcd format
            epd_str = oko_get_full_epd_str(id)
        except:
           print("id {0} not found in database".format(id))
           continue
        
        try:
            #converts to epdx formatted json string
            epdx_str = lcax.convert_ilcd(data = epd_str, as_type = str)

        except:
           print("id {0} could not be converted to epdx".format(id))
           continue
        
        try:
            if isinstance(output, str):
               output = {}
            
            output.update({id : epdx_str})
            print ("saved id {0} to database".format(id))
        except:
           print("id {0} could not be updated".format(id))
           continue

    return output
