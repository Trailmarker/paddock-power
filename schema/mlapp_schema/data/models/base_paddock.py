# -*- coding: utf-8 -*-
from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column

from .mixins import AreaMixin, NameMixin, StatusMixin
from .feature import Feature

from ..names import BUILD_FENCE


class BasePaddock(Feature, AreaMixin, NameMixin, StatusMixin):
    __tablename__ = 'Base Paddocks'

    buildFence = mapped_column(BUILD_FENCE, Integer, nullable=True)
