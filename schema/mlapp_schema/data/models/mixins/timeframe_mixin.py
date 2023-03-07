# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.orm import declared_attr, mapped_column

from ...names import TIMEFRAME


class TimeframeMixin:

    status = mapped_column(TIMEFRAME, String, nullable=False)
