# -*- coding: utf-8 -*-
from geoalchemy2 import Index
from sqlalchemy import Integer
from sqlalchemy.orm import declared_attr, mapped_column

from .feature import Feature
from .mixins import LineMixin, NameMixin, StatusMixin

from ..names import BUILD_ORDER


class Fence(Feature, LineMixin, NameMixin, StatusMixin):
    __tablename__ = 'Fences'

    buildOrder = mapped_column(BUILD_ORDER, Integer, nullable=False)
