# -*- coding: utf-8 -*-
from geoalchemy2 import Geometry
from sqlalchemy import Float
from sqlalchemy.orm import mapped_column

from ...constants import PLUGIN_EPSG
from ..names import GEOMETRY, LENGTH


class LineMixin:

    geometry = mapped_column(
        GEOMETRY,
        (Geometry(
            geometry_type='LINESTRING',
            srid=PLUGIN_EPSG,
            spatial_index=True)),
        nullable=False)
    length = mapped_column(LENGTH, Float, nullable=False)
