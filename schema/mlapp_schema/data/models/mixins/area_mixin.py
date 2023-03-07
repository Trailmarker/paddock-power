# -*- coding: utf-8 -*-
from geoalchemy2 import Geometry, Index
from sqlalchemy import Float
from sqlalchemy.orm import declared_attr, mapped_column

from ...constants import PLUGIN_EPSG
from ...names import AREA, GEOMETRY, PERIMETER


class AreaMixin:

    geometry = mapped_column(
        GEOMETRY,
        (Geometry(
            geometry_type='MULTIPOLYGON',
            srid=PLUGIN_EPSG,
            spatial_index=False)),
        nullable=False)
    area = mapped_column(AREA, Float, nullable=False)
    perimeter = mapped_column(PERIMETER, Float, nullable=False)
