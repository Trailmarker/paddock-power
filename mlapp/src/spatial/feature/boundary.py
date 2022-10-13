# -*- coding: utf-8 -*-
from qgis.core import QgsFeature, QgsFields

from ...models.paddock_power_error import PaddockPowerError
from .area_feature import AreaFeature


class Boundary(AreaFeature):
    SCHEMA = AreaFeature.SCHEMA


BoundaryFeature = type('BoundaryFeature', (Boundary, QgsFeature), {})


def asBoundary(feature):
    """Return a Boundary object from a QgsFeature."""
    if not isinstance(feature, QgsFeature):
        raise PaddockPowerError("asBoundary: feature is not a QgsFeature")
    if not isinstance(feature, Boundary):
        feature.__class__ = BoundaryFeature
    return feature


def makeBoundary():
    """Return a new and empty Boundary object."""
    fields = QgsFields()
    for field in Boundary.SCHEMA:
        fields.append(field)

    feature = QgsFeature(fields)
    return asBoundary(feature)
