# -*- coding: utf-8 -*-
from geoalchemy2 import Index
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import declared_attr, mapped_column, relationship

from .base_paddock import BasePaddock
from .feature import Feature
from .mixins import AreaMixin, TimeframeMixin

from ..names import FID, PADDOCK, WATERED_TYPE


class WateredArea(Feature, AreaMixin, TimeframeMixin):
    __tablename__ = 'Watered Areas'

    paddock = mapped_column(PADDOCK, Integer, ForeignKey(f"{BasePaddock.__tablename__}.{FID}"), nullable=False)
    wateredType = mapped_column(WATERED_TYPE, String, nullable=False)

    paddock_ = relationship(BasePaddock.__tablename__)
