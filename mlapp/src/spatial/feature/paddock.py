# -*- coding: utf-8 -*-
from qgis.core import (QgsFeature, QgsField, QgsFields)
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsFeature

from ...models.paddock_power_error import PaddockPowerError
from ..calculator import Calculator
from .feature import Feature


class Paddock(Feature):
    NAME, AREA, PERIMETER, CONDITION, BUILD_FENCE = ["Paddock Name",
                                                     "Paddock Area (km²)",
                                                     "Paddock Perimeter (km)",
                                                     "Condition",
                                                     "Build Fence"]

    SCHEMA = [
        QgsField(name=NAME, type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=AREA, type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=PERIMETER, type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=CONDITION, type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=BUILD_FENCE, type=QVariant.LongLong, typeName="Integer64",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=Feature.STATUS, type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid)
    ]

    def paddockName(self):
        return str(self[Paddock.NAME])

    def paddockArea(self):
        return self[Paddock.AREA]

    def paddockPerimeter(self):
        return self[Paddock.PERIMETER]

    def paddockCondition(self):
        return str(self[Paddock.CONDITION])

    def paddockBuildFence(self):
        return self[Paddock.BUILD_FENCE]

    def setPaddockName(self, name):
        self.setAttribute(Paddock.NAME, name)

    def setPaddockCondition(self, condition):
        self.setAttribute(Paddock.CONDITION, condition)

    def setPaddockBuildFence(self, buildFence):
        self.setAttribute(Paddock.BUILD_FENCE, buildFence)

    def recalculate(self, elevationLayer=None):
        """Recalculate the area and perimeter of the Paddock."""
        area = round(Calculator.calculateArea(self.geometry()) / 1000000, 2)
        perimeter = round(Calculator.calculatePerimeter(self.geometry()) / 1000, 2)
        self.setAttribute(Paddock.AREA, area)
        self.setAttribute(Paddock.PERIMETER, perimeter)


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
