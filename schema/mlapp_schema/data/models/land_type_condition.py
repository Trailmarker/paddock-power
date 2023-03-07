# -*- coding: utf-8 -*-
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import declared_attr, mapped_column, relationship

from .base_paddock import BasePaddock
from .feature import Feature
from .land_type import LandType
from .mixins import AreaMixin, NameMixin, StatusMixin

from ..names import CONDITION_TYPE, FID, LAND_TYPE, PADDOCK


class LandTypeCondition(Feature, AreaMixin, NameMixin, StatusMixin):
    __tablename__ = 'Land Type Condition Table'

    paddock = mapped_column(PADDOCK, Integer, ForeignKey(f"{BasePaddock.__tablename__}.{FID}"), nullable=False)
    landType = mapped_column(LAND_TYPE, Integer, ForeignKey(f"{LandType.__tablename__}.{FID}"), nullable=False)
    conditionType = mapped_column(CONDITION_TYPE, String, nullable=False)

    paddock_ = relationship(BasePaddock.__tablename__)
    landType_ = relationship(LandType.__tablename__)

    # CONSTRAINT "Unique" PRIMARY KEY ("{PADDOCK}", "{LAND_TYPE}")
    
