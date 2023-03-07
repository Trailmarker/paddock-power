# -*- coding: utf-8 -*-
from geoalchemy2 import Geometry
from sqlalchemy import Float
from sqlalchemy.orm import mapped_column

from ...constants import PLUGIN_EPSG
from ..names import ELEVATION, GEOMETRY, LONGITUDE, LATITUDE


class PointMixin:

    geometry = mapped_column(
        GEOMETRY,
        (Geometry(
            geometry_type='POINT',
            srid=PLUGIN_EPSG,
            spatial_index=True)),
        nullable=False)
    elevation = mapped_column(ELEVATION, Float, nullable=False)
    longitude = mapped_column(LONGITUDE, Float, nullable=False)
    latitude = mapped_column(LATITUDE, Float, nullable=False)
