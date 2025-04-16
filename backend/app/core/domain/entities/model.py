# app/core/domain/entities/model.py
from typing import Dict, Optional
from sqlalchemy import ForeignKey, String, Integer, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.core.domain.entities.base import Base

class Model(Base):
    __tablename__ = 'models'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id_created: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    user_id_updated: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    status: Mapped[str] = mapped_column(String(255), nullable=False)
    model_id: Mapped[str] = mapped_column(String(255), nullable=True)
    model_description: Mapped[str] = mapped_column(String(255), nullable=True)
    model_name: Mapped[str] = mapped_column(String(255), nullable=True)
    model_unit: Mapped[str] = mapped_column(String(255), nullable=True)
    model_quantity: Mapped[float] = mapped_column(Float(20), nullable=True)
    lcax: Mapped[Dict] = mapped_column(JSON, nullable=True)
    model_classification: Mapped[Dict] = mapped_column(JSON, nullable=True)
    model_url: Mapped[str] = mapped_column(String(255), nullable=True)
    model_location: Mapped[str] = mapped_column(String(45), nullable=True)
    model_formatVersion: Mapped[str] = mapped_column(String(45), nullable=True)
    model_lcaMethod: Mapped[str] = mapped_column(String(45), nullable=True)
    model_classificationSystem: Mapped[str] = mapped_column(String(45), nullable=True)
    model_lifeCycleStages: Mapped[Dict] = mapped_column(JSON, nullable=True)
    model_impactCategories: Mapped[Dict] = mapped_column(JSON, nullable=True)
    model_emissionParts: Mapped[Dict] = mapped_column(JSON, nullable=True)
    model_lifeSpan: Mapped[int] = mapped_column(Integer, nullable=True)