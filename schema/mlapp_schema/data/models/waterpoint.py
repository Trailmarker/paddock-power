# -*- coding: utf-8 -*-
from geoalchemy2 import Index
from sqlalchemy import Float, String
from sqlalchemy.orm import declared_attr, mapped_column

from .feature import Feature
from .mixins import NameMixin, PointMixin, StatusMixin

from ..names import WATERPOINT_TYPE, NEAR_GRAZING_RADIUS, FAR_GRAZING_RADIUS


class Waterpoint(Feature, PointMixin, NameMixin, StatusMixin):
    __tablename__ = 'Waterpoints'

    waterpointType = mapped_column(WATERPOINT_TYPE, String, nullable=False)
    nearGrazingRadius = mapped_column(NEAR_GRAZING_RADIUS, Float, nullable=False)
    farGrazingRadius = mapped_column(FAR_GRAZING_RADIUS, Float, nullable=False)
