# -*- coding: utf-8 -*-
from qgis.core import (QgsFeature, QgsField, QgsGeometry, QgsLineString, QgsPoint,
                       QgsWkbTypes)
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsFeature

class Paddock(QgsFeature):
    NAME, AREA, PERIMETER, CONDITION, STATUS = ["Paddock Name",
                                                "Paddock Area (km²)",
                                                "Paddock Perimeter (km)",
                                                "Condition",
                                                "Status"]

    SCHEMA = [
        QgsField(name=NAME, type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=AREA, type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=PERIMETER, type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=CONDITION, type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name=STATUS, type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid)
    ]

    def paddockName(self):
        """Return the name of the paddock."""
        return str(self[self.NAME])

    def paddockArea(self):
        """Return the area of the paddock."""
        return self[self.AREA]

    def paddockPerimeter(self):
        """Return the perimeter of the paddock."""
        return self[self.PERIMETER]

    def setPaddockName(self, name):
        """Set the name of the paddock."""
        self.setAttribute(self.NAME, name)

    def setPaddockArea(self, area):
        """Set the area of the paddock."""
        self.setAttribute(self.AREA, area)

    def setPaddockPerimeter(self, perimeter):
        """Set the perimeter of the paddock."""
        self.setAttribute(self.PERIMETER, perimeter)

def makePaddock(feature):
    """Return a Paddock object from a QgsFeature."""
    feature.__class__ = type('PaddockFeature', (Paddock, QgsFeature), {})
    return feature