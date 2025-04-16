# app/core/domain/entities/user.py
from datetime import datetime
from typing import Dict, List, Optional

from app.core.domain.entities.base import Base
from sqlalchemy import (JSON, Boolean, DateTime, ForeignKey, Integer, String,
                        Text, UniqueConstraint)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_serializer import SerializerMixin


class Category(Base, SerializerMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id_created: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    user_id_updated: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    name: Mapped[str] = mapped_column(
        String(50), unique=False, nullable=False, index=True
    )  # display name
    type: Mapped[str] = mapped_column(
        String(50), unique=False, nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(
        String(50), unique=False, nullable=False, index=True
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text
    )  # tooltip to explain category use
    property_schema: Mapped[Optional[Dict]] = mapped_column(JSON)

    associations: Mapped[Optional[List["CategoryAssociation"]]] = relationship(
        "CategoryAssociation",
        back_populates="category",
        cascade="all, delete-orphan",
        lazy="noload",
    )

    # Add unique constraint for the combination of name and type
    __table_args__ = (UniqueConstraint("name", "type", name="uq_category_name_type"),)

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name}, type={self.type})"
