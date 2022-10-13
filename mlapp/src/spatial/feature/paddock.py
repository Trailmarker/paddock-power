# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsFeature, QgsField, QgsFields

from ...models.paddock_power_error import PaddockPowerError
from .capacity_feature import CapacityFeature


class Paddock(CapacityFeature):
    CONDITION, BUILD_FENCE = ["Condition",
                              "Build Fence"]

    SCHEMA = CapacityFeature.SCHEMA + [
        QgsField(name=CONDITION, type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=BUILD_FENCE, type=QVariant.LongLong, typeName="Integer64",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
    ]

    def paddockCondition(self):
        return str(self[Paddock.CONDITION])

    def paddockBuildFence(self):
        return self[Paddock.BUILD_FENCE]

    def setPaddockCondition(self, condition):
        self.setAttribute(Paddock.CONDITION, condition)

    def setPaddockBuildFence(self, buildFence):
        self.setAttribute(Paddock.BUILD_FENCE, buildFence)


PaddockFeature = type('PaddockFeature', (Paddock, QgsFeature), {})


def asPaddock(feature):
    """Return a Paddock object from a QgsFeature."""
    if not isinstance(feature, QgsFeature):
        raise PaddockPowerError("asPaddock: feature is not a QgsFeature")
    if not isinstance(feature, Paddock):
        feature.__class__ = PaddockFeature
    return feature


def makePaddock():
    """Return a new and empty Paddock object."""
    fields = QgsFields()
    for field in Paddock.SCHEMA:
        fields.append(field)

    feature = QgsFeature(fields)
    return asPaddock(feature)
