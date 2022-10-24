# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtGui import QColor

from qgis.core import QgsWkbTypes

from ...spatial.features.feature import Feature
from ...spatial.features.paddock import Paddock
from ...spatial.selection import Selection


class PaddockSelection(Selection):

    def __init__(self, project, canvas):
        """Constructor."""
        super().__init__(project, canvas, QgsWkbTypes.PolygonGeometry)

    def styleUi(self):
        paddockColour = QColor("green")
        paddockColour.setAlphaF(0.4)

        self.setWidth(4)
        self.setColor(paddockColour)
        self.setFillColor(paddockColour)

    @pyqtSlot(Feature)
    def setSelectedFeature(self, feature):
        if isinstance(feature, Paddock):
            super().setSelectedFeature(feature)
