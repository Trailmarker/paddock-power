# -*- coding: utf-8 -*-
from ..calculator import Calculator
from .feature import Feature


class LineFeature(Feature):
    LENGTH = "Length (km)"

    def featureLength(self):
        return self[LineFeature.LENGTH]

    def recalculate(self, elevationLayer=None):
        """Recalculate the length of this Pipeline."""
        self.profile = Calculator.calculateProfile(
            self.geometry(), elevationLayer)
        length = round(self.profile.maximumDistance, 2)
        self.setAttribute(LineFeature.LENGTH, length)
