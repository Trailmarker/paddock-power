from sqlalchemy import Float, String
# -*- coding: utf-8 -*-
from sqlalchemy.orm import mapped_column

from .feature import Feature
from .mixins import AreaMixin
from ..names import LAND_TYPE_NAME, OPTIMAL_CAPACITY_PER_AREA


class LandType(Feature, AreaMixin):
    __tablename__ = 'Land Types'

    landTypeName = mapped_column(LAND_TYPE_NAME, String, nullable=False)
    optimalCapacityPerArea = mapped_column(OPTIMAL_CAPACITY_PER_AREA, Float, nullable=False)
