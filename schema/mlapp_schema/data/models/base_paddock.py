# -*- coding: utf-8 -*-
from geoalchemy2 import Index
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import declared_attr, mapped_column, relationship

from .feature import Feature
from .fence import Fence
from .mixins import AreaMixin, NameMixin, StatusMixin

from ..names import BUILD_FENCE, FID


class BasePaddock(Feature, AreaMixin, NameMixin, StatusMixin):
    __tablename__ = 'Base Paddocks'

    buildFence = mapped_column(BUILD_FENCE, Integer, ForeignKey(f"{Fence.__tablename__}.{FID}"), nullable=True)
    
    buildFence_ = relationship(Fence.__tablename__)
