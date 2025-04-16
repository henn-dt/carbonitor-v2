# backend/app/core/domain/entities/model_mapping.py

from typing import Dict, Optional

from app.core.domain.entities.base import Base
from sqlalchemy import JSON, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin


class FilterMapping(Base, SerializerMixin):
    __tablename__ = 'mappings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id_created: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    user_id_updated: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    status: Mapped[str] = mapped_column(String(255), nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)   # software
    source_version: Mapped[str] = mapped_column(String(255), nullable=False) # software version
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # buildup, model, other, ..
    maps: Mapped[Dict] = mapped_column(JSON, nullable=True) # ProductMappingElements or BuildupMappingElement


"""
example of use:

mapping.name = "rhino_buildups_henn_standard"
mapping.source = "Rhino"
mapping.source_version = "8"
mapping.maps = {"Glass" : {"id" : "Glass", 
                            "filter" : {<Filter Data as JSON>},
                            "impact_data" : [
                                        {"uri" : "Oekobaudat.e94dbfcc-56f2-4e55-8e0e-c2e8a2b576ae,
                                         "quantity" : 1},
                                            ]
                            }
                {"Steel-Extrusion" : {"id" : "Steel-Extrusion", 
                            "filter" : {<Filter Data as JSON>},
                            "impact_data" : [
                                        {"uri" : "Oekobaudat.755a481d-a74b-4ba0-b417-cc26767b2d50,
                                         "quantity" : 1},
                                            ]
                            }
                } 
"""