from sqlalchemy import Integer, String
# -*- coding: utf-8 -*-
from sqlalchemy.orm import mapped_column

from .feature import Feature
from .mixins import AreaMixin, TimeframeMixin

from .names import PADDOCK, WATERED_TYPE


class WateredArea(Feature, AreaMixin, TimeframeMixin):
    __tablename__ = 'Watered Areas'

    paddock = mapped_column(PADDOCK, Integer, nullable=False)
    wateredType = mapped_column(WATERED_TYPE, String, nullable=False)
