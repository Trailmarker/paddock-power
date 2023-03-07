# -*- coding: utf-8 -*-
from sqlalchemy import Float
from sqlalchemy.orm import mapped_column

from ..names import ESTIMATED_CAPACITY, ESTIMATED_CAPACITY_PER_AREA, POTENTIAL_CAPACITY, POTENTIAL_CAPACITY_PER_AREA, WATERED_AREA
from .area_mixin import AreaMixin
from .timeframe_mixin import TimeframeMixin


class CapacityMixin(AreaMixin, TimeframeMixin):

    wateredArea = mapped_column(WATERED_AREA, Float, nullable=False)
    estimatedCapacityPerArea = mapped_column(ESTIMATED_CAPACITY_PER_AREA, Float, nullable=False)
    potentialCapcityPerArea = mapped_column(POTENTIAL_CAPACITY_PER_AREA, Float, nullable=False)
    estimatedCapacity = mapped_column(ESTIMATED_CAPACITY, Float, nullable=False)
    potentialCapacity = mapped_column(POTENTIAL_CAPACITY, Float, nullable=False)
