# -*- coding: utf-8 -*-
from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import mapped_column

from .base_paddock import BasePaddock
from .feature import Feature
from .mixins import AreaMixin, StatusMixin, TimeframeMixin
from .waterpoint import Waterpoint

from ..names import WATERPOINT, PADDOCK, GRAZING_RADIUS_TYPE, GRAZING_RADIUS
from ..utils import fidForeignKey


class WaterpointBuffer(Feature, AreaMixin, StatusMixin, TimeframeMixin):
    __tablename__ = 'Waterpoint Buffers'

    waterpoint = mapped_column(WATERPOINT, Integer, nullable=False)
    paddock = mapped_column(PADDOCK, Integer, nullable=False)
    grazingRadiusType = mapped_column(GRAZING_RADIUS_TYPE, String, nullable=False)
    grazingRadius = mapped_column(GRAZING_RADIUS, Float, nullable=False)

    fkWaterpoint = fidForeignKey(WATERPOINT, Waterpoint)
    fkPaddock = fidForeignKey(PADDOCK, BasePaddock)
