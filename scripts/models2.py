# coding: utf-8
from sqlalchemy import Column, DateTime, Float, Integer, JSON, MetaData, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata



class Buildup(Base):
    __tablename__ = 'buildups'

    id = Column(Integer, primary_key=True)
    status = Column(String(255), nullable=False, server_default=FetchedValue())
    user_created = Column(String(36))
    date_created = Column(DateTime)
    user_updated = Column(String(36))
    date_updated = Column(DateTime)
    buildup_id = Column(String(255))
    buildup_description = Column(String(255))
    buildup_name = Column(String(255))
    buildup_unit = Column(String(255))
    buildup_parts = Column(JSON)
    buildup_classification = Column(JSON)
    buildup_url = Column(String(255))
    buildup_quantity = Column(Float(20))



class Model(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True)
    status = Column(String(255), nullable=False, server_default=FetchedValue())
    user_created = Column(String(36))
    date_created = Column(DateTime)
    user_updated = Column(String(36))
    date_updated = Column(DateTime)
    model_id = Column(String(255))
    model_description = Column(String(255))
    model_name = Column(String(255))
    model_unit = Column(String(255))
    model_quantity = Column(Float(20))
    lcax = Column(JSON)
    model_classification = Column(JSON)
    model_url = Column(String(255))
    model_location = Column(String(45))
    model_formatVersion = Column(String(45))
    model_lcaMethod = Column(String(45))
    model_classificationSystem = Column(String(45))
    model_lifeCycleStages = Column(JSON)
    model_impactCategories = Column(JSON)
    model_emissionParts = Column(JSON)
    model_lifeSpan = Column(Integer)



class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    status = Column(String(255), nullable=False, server_default=FetchedValue())
    user_created = Column(String(36))
    date_created = Column(DateTime)
    user_updated = Column(String(36))
    date_updated = Column(DateTime)
    epd_name = Column(String(255))
    epd_declaredUnit = Column(String(255))
    epd_version = Column(String(255))
    epd_publishedDate = Column(String(255))
    epd_validUntil = Column(String(255))
    epd_standard = Column(String(255))
    epd_comment = Column(String(255))
    epd_location = Column(String(255))
    epd_formatVersion = Column(String(45))
    epd_id = Column(String(255))
    epdx = Column(JSON)
    epd_sourceName = Column(String(255))
    epd_sourceUrl = Column(String(255))
    epd_linear_density = Column(Float(10))
    epd_gross_density = Column(Float(10))
    epd_grammage = Column(Float(10))
    epd_layer_thickness = Column(Float(10))
    epd_subtype = Column(String(255))
    epd_bulk_density = Column(Float(10))
