# -*- coding: utf-8 -*-
from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column

from ..constants import PLUGIN_NAME
from ..base import Base
from .names import FID


class Feature(Base):
    f"""Model a {PLUGIN_NAME} feature."""

    __abstract__ = True

    fid = mapped_column(FID, Integer, primary_key=True, nullable=False)
