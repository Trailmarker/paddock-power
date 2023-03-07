# -*- coding: utf-8 -*-
from sqlalchemy.orm import declared_attr
from geoalchemy2 import Index
from .feature import Feature
from .mixins import AreaMixin, TimeframeMixin


class Boundary(Feature, AreaMixin, TimeframeMixin):
    __tablename__ = 'Boundary'
