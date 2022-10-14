# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QColor

from qgis.core import QgsWkbTypes

from ...spatial.selection import Selection


class PaddockSelection(Selection):

    def __init__(self, canvas, parent=None):
        """Constructor."""
        super().__init__(canvas, QgsWkbTypes.PolygonGeometry)

    def styleUi(self):
        paddockColour = QColor("green")
        paddockColour.setAlphaF(0.4)

        self.setWidth(4)
        self.setColor(paddockColour)
        self.setFillColor(paddockColour)
