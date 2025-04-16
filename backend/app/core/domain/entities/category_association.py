from typing import Dict, List, Optional

from app.core.domain.entities.base import Base
from sqlalchemy import JSON, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_serializer import SerializerMixin


class CategoryAssociation(Base, SerializerMixin):
    __tablename__ = "category_associations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    entity_id: Mapped[int] = mapped_column(Integer, nullable=False)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g. 'product', 'buildup', or 'model'
    values: Mapped[Optional[Dict]] = mapped_column(JSON, nullable=True)  # Store entity-specific category values

    category = relationship("Category", back_populates="associations", lazy="joined")

    # Create a unique constraint to prevent duplicate associations
    __table_args__ = (UniqueConstraint("category_id", "entity_id", "entity_type", name="uix_category_entity"),)

    def __repr__(self):
        return f"<CategoryAssociation(id={self.id}, category_id={self.category_id}, entity_type='{self.entity_type}', entity_id={self.entity_id})>"
