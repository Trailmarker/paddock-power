# -*- coding: utf-8 -*-
from qgis.core import (QgsFeature, QgsField, QgsFields)
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsFeature

from .calculator import Calculator
from .paddock_power_feature import PaddockPowerFeature


class Paddock(PaddockPowerFeature):
    NAME, AREA, PERIMETER, CONDITION = ["Paddock Name",
                                        "Paddock Area (km²)",
                                        "Paddock Perimeter (km)",
                                        "Condition"]

    SCHEMA = [
        QgsField(name=NAME, type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=AREA, type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=PERIMETER, type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=CONDITION, type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=PaddockPowerFeature.STATUS, type=QVariant.String, typeName="String",
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

    def setPaddockName(self, name):
        self.setAttribute(Paddock.NAME, name)

    def setPaddockCondition(self, condition):
        self.setAttribute(Paddock.CONDITION, condition)

    def calculate(self, elevationLayer=None):
        """Recalculate the area and perimeter of the Paddock."""
        area = Calculator.calculateArea(self.geometry())
        perimeter = Calculator.calculatePerimeter(self.geometry())
        self.setPaddockArea(area)
        self.setPaddockPerimeter(perimeter)




def asPaddock(feature):
    """Return a Paddock object from a QgsFeature."""
    feature.__class__ = type('PaddockFeature', (Paddock, QgsFeature), {})
    return feature


def makePaddock():
    """Return a new and empty Paddock object."""
    fields = QgsFields()
    for field in Paddock.SCHEMA:
        fields.append(field)

    feature = QgsFeature(fields)
    return asPaddock(feature)
