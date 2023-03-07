# -*- coding: utf-8 -*-
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from .base_paddock import BasePaddock
from .feature import Feature
from .land_type import LandType
from .mixins import CapacityMixin

from ..names import PADDOCK, LAND_TYPE, PADDOCK_NAME, LAND_TYPE_NAME, CONDITION_TYPE
from ..utils import fidForeignKey


class PaddockLandType(Feature, CapacityMixin):
    __tablename__ = 'Paddock Land Types'

    paddock = mapped_column(PADDOCK, Integer, nullable=False)
    landType = mapped_column(LAND_TYPE, Integer, nullable=False)
    paddockName = mapped_column(PADDOCK_NAME, String, nullable=False)
    landTypeName = mapped_column(LAND_TYPE_NAME, String, nullable=False)
    conditionType = mapped_column(CONDITION_TYPE, String, nullable=False)

    fkPaddock = fidForeignKey(PADDOCK, BasePaddock)
    fkLandType = fidForeignKey(LAND_TYPE, LandType)
