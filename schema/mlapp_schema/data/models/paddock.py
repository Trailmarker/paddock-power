# -*- coding: utf-8 -*-
from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column

from .mixins import CapacityMixin, NameMixin, StatusMixin
from .feature import Feature

from .names import BUILD_FENCE, PADDOCK


class Paddock(Feature, CapacityMixin, NameMixin, StatusMixin):
    __tablename__ = 'Paddocks'

    paddock = mapped_column(PADDOCK, Integer, nullable=False)
    buildFence = mapped_column(BUILD_FENCE, Integer, nullable=True)
