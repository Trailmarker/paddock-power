from abc import ABC, ABCMeta
# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta


class DeclarativeABCMeta(DeclarativeMeta, ABCMeta):
    """Declare a metaclass that mixes in the ABCMeta metaclass with the default for declarative_base()."""
    pass


class Base(declarative_base(metaclass=DeclarativeABCMeta)):
    """Base class for all models."""
    __abstract__ = True
