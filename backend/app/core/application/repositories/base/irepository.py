# app/core/application/repositories/base/irepository.py
from abc import ABC
from typing import Generic, TypeVar

T = TypeVar('T')
K = TypeVar('K')

class IRepository(ABC, Generic[T]):
    """Base repository interface"""
    pass