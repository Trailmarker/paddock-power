# -*- coding: utf-8 -*-
from geoalchemy2 import Index
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import declared_attr, mapped_column, relationship

from .base_paddock import BasePaddock
from .fence import Fence
from .feature import Feature
from .mixins import CapacityMixin, NameMixin, StatusMixin

from ..names import FID, BUILD_FENCE, PADDOCK


class Paddock(Feature, CapacityMixin, NameMixin, StatusMixin):
    __tablename__ = 'Paddocks'

    paddock = mapped_column(PADDOCK, Integer, ForeignKey(f"{BasePaddock.__tablename__}.{FID}"), nullable=False)
    buildFence = mapped_column(BUILD_FENCE, Integer, ForeignKey(f"{Fence.__tablename__}.{FID}"), nullable=True)

    paddock_ = relationship(BasePaddock.__tablename__)
    buildFence_ = relationship(Fence.__tablename__)
