# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsFeature, QgsField, QgsFields

from ...models.paddock_power_error import PaddockPowerError
from .capacity_feature import CapacityFeature


class LandSystem(CapacityFeature):

    MAP_UNIT = "Map Unit"
    LANDSCAPE_CLASS = "Landscape Class"
    CLASS_DESCRIPTION = "Class Description"
    EROSION_RISK = "Erosion Risk"

    SCHEMA = CapacityFeature.SCHEMA + [
        QgsField(name="Map Unit", type=QVariant.String, typeName="String",
                 len=10, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Landscape Class", type=QVariant.String, typeName="String",
                 len=50, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Class Description", type=QVariant.String, typeName="String",
                 len=254, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Erosion Risk", type=QVariant.String, typeName="String",
                 len=100, prec=0, comment="", subType=QVariant.Invalid)
    ]


LandSystemFeature = type('LandSystemFeature', (LandSystem, QgsFeature), {})


def asLandSystem(feature):
    """Return a LandSystem object from a QgsFeature."""
    if not isinstance(feature, QgsFeature):
        raise PaddockPowerError("asLandSystem: feature is not a QgsFeature")
    if not isinstance(feature, LandSystem):
        feature.__class__ = LandSystemFeature
    return feature


def makeLandSystem():
    """Return a new and empty LandSystem object."""
    fields = QgsFields()
    for field in LandSystem.SCHEMA:
        fields.append(field)

    feature = QgsFeature(fields)
    return asLandSystem(feature)
