"""Пакет с модулями лабораторной работы."""

from .database import DatabaseRepository
from .parser import ForumParser

__all__ = ["DatabaseRepository", "ForumParser"]