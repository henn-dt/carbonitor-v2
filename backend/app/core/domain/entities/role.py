# app/core/domain/entities/role.py
from sqlalchemy import JSON, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.domain.entities.base import Base

class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    permissions: Mapped[list] = mapped_column(JSON, nullable=True, default=None)