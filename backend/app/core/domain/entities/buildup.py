# app/core/domain/entities/buildup.py
from typing import Dict, List, Optional
from sqlalchemy import ForeignKey, String, Integer, Float, JSON, text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.domain.entities.base import Base
from sqlalchemy_serializer import SerializerMixin

class Buildup(Base, SerializerMixin):
    __tablename__ = 'buildups'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id_created: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    user_id_updated: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    status: Mapped[str] = mapped_column(String(255), nullable=False)
    classification: Mapped[Optional[List[Dict]]] = mapped_column(JSON, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    quantity: Mapped[float] = mapped_column(Float(10), server_default=text("1.0") )
    unit: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    meta_data: Mapped[Optional[Dict]] = mapped_column(JSON, nullable=True)
    products: Mapped[Dict] = mapped_column(JSON, nullable=True)
    results: Mapped[Dict] = mapped_column(JSON, nullable=True)


""" 
examples of use:

example meta_data:  
buildup.meta_data = {"model_mapping": "revit_buildup_henn_default", "model_url" : 'https://speckle.henn.com/streams/8184ae17b5/commits/7caaac3ea0' }

example classification:
buildup.classification = [{"code": 337, "name": "Elementierte Aussenwandkonstruktion", "system": "DIN277"}, {"code": 4000, "name": "Fassade", "system": "HENN"}]


example products:

### for product reference ###
buildup.products = {
"product_id_1" :
{
"overrides" = {"meta_data" : {"model_mapping_element_id" : "Gipskarton 2-lagig"}},
"type" = "reference",
"uri" = "Oekobaudat.deeb0bda-20fa-412a-b945-1a589638db21"
},
"product_id_2" :
{
"overrides" = {"meta_data" : {"model_mapping_element_id" : "Mineralwolle"}},
"type" = "reference",
"uri" = "Oekobaudat.50d421e2-3a7b-4659-92a4-f20d6a52fcf0"
},
"product_id_3" :
{
"overrides" = {"meta_data" : {"model_mapping_element_id" : "Stahl für Ständerwerk CW Profil 10cm"}},
"type" = "reference",
"uri" = "Oekobaudat.800dc37d-c3a2-4b12-b14b-54f7bc775f47"
}}



### for actual product snapshot data ####
buildup.products = {     
"product_id_1" :
{ 
"id" : "f6861618-5a92-4c3a-94ba-9f7329b29662"
"source" : {"source_name" : "Oekobaudat", "source_url" : "url_to_epd"},
"type" : "actual",
"meta_data" : {"model_mapping_element_id" : "Transportbeton"}
"impacts" : {<actual impact data>},
<all other EPD properties>
}
}

example results:

buildup.results = {  "product_id_1": {"quantity": 40},  "product_id_2": {"quantity": 9},  "product_id_3": {"quantity": 14.4}}

"""