# app/core/domain/entities/product.py
from typing import Dict, Optional

from app.core.domain.entities.base import Base
from sqlalchemy import JSON, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin


class FilterElement(Base, SerializerMixin):
    __tablename__ = 'filters'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id_created: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    user_id_updated: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    status: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)    # user defined name for the filter
    source: Mapped[str] = mapped_column(String(255), nullable=False)   # software
    source_version: Mapped[str] = mapped_column(String(255), nullable=False) # software version
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # buildup, model, other, ..
    filter: Mapped[Dict] = mapped_column(JSON, nullable=True) # the JSON serialisation of the desktop filter object

        

