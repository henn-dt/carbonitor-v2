# app/core/domain/entities/user_roles.py
from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.domain.entities.base import Base

user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
)