# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant

from qgis.core import QgsFeature, QgsField

from ...calculator import Calculator
from ...layer.elevation_layer import ElevationLayer
from .feature import Feature

class LineFeature(Feature):
    LENGTH = "Length (km)"

    SCHEMA = Feature.SCHEMA + [
        QgsField(name=LENGTH, type=QVariant.Double, typeName="Real",
                 len=0, prec=0, comment="", subType=QVariant.Invalid)
    ]

    def __init__(self, feature: QgsFeature=None, elevationLayer: ElevationLayer=None):
        """Create a new LineFeature."""
        super().__init__(feature)

        assert elevationLayer is None or isinstance(elevationLayer, ElevationLayer), "elevationLayer must be provided"

        self.elevationLayer = elevationLayer
        self.profile = None
        self.recalculate()

    def featureLength(self):
        return self[LineFeature.LENGTH]

    def recalculate(self):
        """Recalculate the length of this Pipeline."""
        self.profile = Calculator.calculateProfile(
            self.geometry(), self.elevationLayer)
        length = round(self.profile.maximumDistance / 1000, 2)
        self.setAttribute(LineFeature.LENGTH, length)
