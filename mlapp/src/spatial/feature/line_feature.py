# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsField

from ..calculator import Calculator
from .feature import Feature


class LineFeature(Feature):
    LENGTH = "Length (km)"

    SCHEMA = Feature.SCHEMA + [
        QgsField(name=LENGTH, type=QVariant.Double, typeName="Real",
                 len=0, prec=0, comment="", subType=QVariant.Invalid)
    ]

    def featureLength(self):
        return self[LineFeature.LENGTH]

    def recalculate(self, elevationLayer=None):
        """Recalculate the length of this Pipeline."""
        self.profile = Calculator.calculateProfile(
            self.geometry(), elevationLayer)
        length = round(self.profile.maximumDistance, 2)
        self.setAttribute(LineFeature.LENGTH, length)
