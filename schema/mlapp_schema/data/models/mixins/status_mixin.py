# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from ...names import STATUS


class StatusMixin:

    status = mapped_column(STATUS, String, nullable=False)
