# -*- coding: utf-8 -*-
from sqlalchemy.orm import declared_attr
from geoalchemy2 import Index
from .feature import Feature
from .mixins import LineMixin, NameMixin, StatusMixin


class Pipeline(Feature, LineMixin, NameMixin, StatusMixin):
    __tablename__ = 'Pipelines'
