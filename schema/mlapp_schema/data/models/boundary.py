# -*- coding: utf-8 -*-
from .feature import Feature
from .mixins import AreaMixin, TimeframeMixin


class Boundary(Feature, AreaMixin, TimeframeMixin):
    __tablename__ = 'Boundary'
