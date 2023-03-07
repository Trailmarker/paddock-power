# -*- coding: utf-8 -*-
from geoalchemy2 import Index
from sqlalchemy import Integer
from sqlalchemy.orm import declared_attr, mapped_column

from ..constants import PLUGIN_NAME
from ..base import Base
from ..names import FID


class Feature(Base):
    f"""Model a {PLUGIN_NAME} feature."""

    __abstract__ = True

    fid = mapped_column(FID, Integer, primary_key=True, nullable=False)
