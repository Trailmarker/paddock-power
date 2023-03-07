# -*- coding: utf-8 -*-
from .feature import Feature
from .mixins import LineMixin, NameMixin, StatusMixin


class Pipeline(Feature, LineMixin, NameMixin, StatusMixin):
    __tablename__ = 'Pipelines'
