# -*- coding: utf-8 -*-
from geoalchemy2 import Index
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import declared_attr, mapped_column, relationship

from .base_paddock import BasePaddock
from .feature import Feature
from .mixins import AreaMixin, StatusMixin, TimeframeMixin
from .waterpoint import Waterpoint

from ..names import FID, WATERPOINT, PADDOCK, GRAZING_RADIUS_TYPE, GRAZING_RADIUS


class WaterpointBuffer(Feature, AreaMixin, StatusMixin, TimeframeMixin):
    __tablename__ = 'Waterpoint Buffers'

    waterpoint = mapped_column(WATERPOINT, Integer, ForeignKey(f"{Waterpoint.__tablename__}.{FID}"), nullable=False)
    paddock = mapped_column(PADDOCK, Integer, ForeignKey(f"{BasePaddock.__tablename__}.{FID}"), nullable=False)
    grazingRadiusType = mapped_column(GRAZING_RADIUS_TYPE, String, nullable=False)
    grazingRadius = mapped_column(GRAZING_RADIUS, Float, nullable=False)

    waterpoint_ = relationship(Waterpoint.__tablename__)
    paddock_ = relationship(BasePaddock.__tablename__)
