# -*- coding: utf-8 -*-
from geoalchemy2 import Index
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import declared_attr, mapped_column, relationship

from .base_paddock import BasePaddock
from .feature import Feature
from .land_type import LandType
from .mixins import CapacityMixin

from ..names import FID, PADDOCK, LAND_TYPE, PADDOCK_NAME, LAND_TYPE_NAME, CONDITION_TYPE


class PaddockLandType(Feature, CapacityMixin):
    __tablename__ = 'Paddock Land Types'

    paddock = mapped_column(PADDOCK, Integer, ForeignKey(f"{BasePaddock.__tablename__}.{FID}"), nullable=False)
    landType = mapped_column(LAND_TYPE, Integer, ForeignKey(f"{LandType.__tablename__}.{FID}"), nullable=False)
    paddockName = mapped_column(PADDOCK_NAME, String, nullable=False)
    landTypeName = mapped_column(LAND_TYPE_NAME, String, nullable=False)
    conditionType = mapped_column(CONDITION_TYPE, String, nullable=False)

    paddock_ = relationship(BasePaddock.__tablename__)
    landType_ = relationship(LandType.__tablename__)
