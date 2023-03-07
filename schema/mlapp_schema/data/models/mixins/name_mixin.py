# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from ...names import NAME


class NameMixin:

    status = mapped_column(NAME, String, nullable=False)
