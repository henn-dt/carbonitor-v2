# app/core/domain/entities/product.py
from typing import Dict, Optional

from app.core.domain.entities.base import Base
from sqlalchemy import JSON, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin


class Product(Base, SerializerMixin):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id_created: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    user_id_updated: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    status: Mapped[str] = mapped_column(String(255), nullable=False)
    epd_name: Mapped[str] = mapped_column(String(255))
    epd_declaredUnit: Mapped[str] = mapped_column(String(255))
    epd_version: Mapped[str] = mapped_column(String(255))
    epd_publishedDate: Mapped[str] = mapped_column(String(255), nullable=True)
    epd_validUntil: Mapped[str] = mapped_column(String(255), nullable=True)
    epd_standard: Mapped[str] = mapped_column(String(255), nullable=True)
    epd_comment: Mapped[str] = mapped_column(String(255), nullable=True)
    epd_location: Mapped[str] = mapped_column(String(255), nullable=True)
    epd_formatVersion: Mapped[str] = mapped_column(String(45), nullable=True)
    epd_id: Mapped[str] = mapped_column(String(255))
    epdx: Mapped[Dict] = mapped_column(JSON)
    epd_sourceName: Mapped[str] = mapped_column(String(255))
    epd_sourceUrl: Mapped[str] = mapped_column(String(255), nullable=True)
    epd_linear_density: Mapped[Optional[float]] = mapped_column(Float(10), nullable=True)
    epd_gross_density: Mapped[Optional[float]] = mapped_column(Float(10), nullable=True)
    epd_grammage: Mapped[Optional[float]] = mapped_column(Float(10), nullable=True)
    epd_layer_thickness: Mapped[Optional[float]] = mapped_column(Float(10), nullable=True)
    epd_subtype: Mapped[str] = mapped_column(String(255), nullable=True)
    epd_bulk_density: Mapped[Optional[float]] = mapped_column(Float(10), nullable=True)
    epd_description: Mapped[Optional[Text]] = mapped_column(Text, nullable = True)