# models/base.py
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Column, DateTime
from enum import Enum

class DatabaseType(Enum):
    USERS = "users"
    CARBONITOR_DATA = "henn_carbonitor"

UserBase = declarative_base()
AppBase = declarative_base()

class TimestampMixin:
    """Mixin for created_at and updated_at columns"""
    date_created = Column(DateTime, nullable=False, default=datetime.now)
    date_updated = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)