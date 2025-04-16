# app/core/domain/entities/__init__.py
from app.core.domain.entities.base import Base
from app.core.domain.entities.buildup import Buildup
from app.core.domain.entities.category import Category
from app.core.domain.entities.category_association import CategoryAssociation
from app.core.domain.entities.identity_provider import IdentityProvider
from app.core.domain.entities.model import Model
from app.core.domain.entities.product import Product
from app.core.domain.entities.role import Role
from app.core.domain.entities.user import User
from app.core.domain.entities.user_identity import UserIdentity
from app.core.domain.entities.user_roles import user_roles
from app.core.domain.entities.filter_element import FilterElement

__all__ = [
    "User",
    "Role",
    "IdentityProvider",
    "UserIdentity",
    "user_roles",
    "Buildup",
    "Model",
    "Product",
    "Category",
    "CategoryAssociation",
    "FilterElement"
]

# app/core/domain/entities/base.py
from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now
    )


# app/core/domain/entities/buildup.py
from typing import Dict, Optional

from app.core.domain.entities.base import Base
from sqlalchemy import JSON, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Buildup(Base):
    __tablename__ = "buildups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id_created: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    user_id_updated: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    status: Mapped[str] = mapped_column(String(255), nullable=False)
    buildup_id: Mapped[str] = mapped_column(String(255), nullable=True)
    buildup_description: Mapped[str] = mapped_column(String(255))
    buildup_name: Mapped[str] = mapped_column(String(255))
    buildup_unit: Mapped[str] = mapped_column(String(255))
    buildup_parts: Mapped[Dict] = mapped_column(JSON)
    buildup_classification: Mapped[Dict] = mapped_column(JSON)
    buildup_url: Mapped[str] = mapped_column(String(255), nullable=True)
    buildup_quantity: Mapped[float] = mapped_column(Float(20), nullable=True)


# app/core/domain/entities/identity_provider.py
from typing import Dict

from app.core.domain.entities.base import Base
from sqlalchemy import JSON, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class IdentityProvider(Base):
    __tablename__ = "identity_providers"

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

# app/core/domain/entities/model.py
from typing import Dict, Optional

from app.core.domain.entities.base import Base
from sqlalchemy import JSON, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Model(Base):
    __tablename__ = "models"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id_created: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    user_id_updated: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
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


# app/core/domain/entities/product.py
from typing import Dict, Optional

from app.core.domain.entities.base import Base
from sqlalchemy import JSON, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id_created: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    user_id_updated: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
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
    epd_linear_density: Mapped[Optional[float]] = mapped_column(
        Float(10), nullable=True
    )
    epd_gross_density: Mapped[Optional[float]] = mapped_column(Float(10), nullable=True)
    epd_grammage: Mapped[Optional[float]] = mapped_column(Float(10), nullable=True)
    epd_layer_thickness: Mapped[Optional[float]] = mapped_column(
        Float(10), nullable=True
    )
    epd_subtype: Mapped[str] = mapped_column(String(255), nullable=True)
    epd_bulk_density: Mapped[Optional[float]] = mapped_column(Float(10), nullable=True)


from app.core.domain.entities.base import Base

# app/core/domain/entities/role.py
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)


from datetime import datetime

# app/core/domain/entities/user_identity.py
from typing import Dict, Optional

from app.core.domain.entities.base import Base
from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class UserIdentity(Base):
    __tablename__ = "user_identities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    provider_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("identity_providers.id")
    )
    external_id: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    data: Mapped[Dict] = mapped_column(JSON)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    __table_args__ = (
        UniqueConstraint("provider_id", "external_id", name="uix_provider_external_id"),
    )


from app.core.domain.entities.base import Base

# app/core/domain/entities/user_roles.py
from sqlalchemy import Column, ForeignKey, Integer, Table

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)

from datetime import datetime

# app/core/domain/entities/user.py
from typing import Optional

from app.core.domain.entities.base import Base
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    auth_method: Mapped[str] = mapped_column(String(20), default="local")
    last_token_issued: Mapped[Optional[datetime]] = mapped_column(DateTime)
    token_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime)


from datetime import datetime

# app/core/domain/entities/user.py
from typing import Optional

from app.core.domain.entities.base import Base
from sqlalchemy import JSON, Boolean, DateTime, Dict, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


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
        String(50), unique=True, nullable=False, index=True
    )  # display name
    type: Mapped[str] = mapped_column(
        String(50), unique=False, nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(
        String(50), unique=False, nullable=False, index=True
    )
    description: Mapped[Optional[str]] = mapped_column(
        String(255)
    )  # tooltip to explain category use
    property_schema: Mapped[Optional[Dict]] = mapped_column(JSON)

    associations: Mapped[Optional[List["CategoryAssociation"]]] = relationship(
        "CategoryAssociation", back_populates="category", cascade="all, delete-orphans"
    )

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name}, type={self.type})"


from typing import Dict, Optional

from app.core.domain.entities.base import Base
from sqlalchemy import JSON, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_serializer import SerializerMixin


class CategoryAssociation(Base, SerializerMixin):
    __tablename__ = "category_associations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categories.id"), nullable=False
    )
    entity_id: Mapped[int] = mapped_column(Integer, nullable=False)
    entity_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # e.g. 'product', 'buildup', or 'model'
    values: Mapped[Optional[Dict]] = mapped_column(
        JSON, nullable=True
    )  # Store entity-specific category values

    category = relationship("Category", back_populates="associations")

    # Create a unique constraint to prevent duplicate associations
    __table_args__ = (
        UniqueConstraint(
            "category_id", "entity_id", "entity_type", name="uix_category_entity"
        ),
    )

    def __repr__(self):
        return f"<CategoryAssociation(id={self.id}, category_id={self.category_id}, entity_type='{self.entity_type}', entity_id={self.entity_id})>"
