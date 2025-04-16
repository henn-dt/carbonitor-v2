# app/core/domain/entities/user_identity.py
from typing import Dict, Optional
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.core.domain.entities.base import Base

class UserIdentity(Base):
    __tablename__ = 'user_identities'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    provider_id: Mapped[int] = mapped_column(Integer, ForeignKey('identity_providers.id'))
    external_id: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    data: Mapped[Dict] = mapped_column(JSON)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    __table_args__ = (
        UniqueConstraint('provider_id', 'external_id', name='uix_provider_external_id'),
    )