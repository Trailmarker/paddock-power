# -*- coding: utf-8 -*-
from geoalchemy2 import Geometry, Index
from sqlalchemy import Float
from sqlalchemy.orm import declared_attr, mapped_column

from ...constants import PLUGIN_EPSG
from ...names import GEOMETRY, LENGTH


class LineMixin:

    geometry = mapped_column(
        GEOMETRY,
        (Geometry(
            geometry_type='LINESTRING',
            srid=PLUGIN_EPSG,
            spatial_index=False)),
        nullable=False)
    length = mapped_column(LENGTH, Float, nullable=False)
