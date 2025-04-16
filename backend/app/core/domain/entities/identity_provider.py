# app/core/domain/entities/identity_provider.py
from typing import Dict
from sqlalchemy import String, Integer, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.core.domain.entities.base import Base

class IdentityProvider(Base):
    __tablename__ = 'identity_providers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    config: Mapped[Dict] = mapped_column(JSON)

# this table is for an API client configuration for each authentication service
# identity_provider record for Google OAuth
# {
#     id: 1,
#     name: "Google",
#     enabled: True,
#     config: {
#         "client_id": "xxx.apps.googleusercontent.com",
#         "client_secret": "yyy",
#         "redirect_uri": "https://yourapp.com/auth/google/callback",
#         "scopes": ["email", "profile"]
#     }
# }

# # identity_provider record for GitHub OAuth
# {
#     id: 2,
#     name: "GitHub",
#     enabled: True,
#     config: {
#         "client_id": "aaa",
#         "client_secret": "bbb",
#         "redirect_uri": "https://yourapp.com/auth/github/callback",
#         "scopes": ["user:email"]
#     }
# }