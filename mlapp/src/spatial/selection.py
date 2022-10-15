# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSlot

from qgis.core import QgsFeature, QgsWkbTypes
from qgis.gui import QgsRubberBand

from ..models.paddock_power_error import PaddockPowerError

class Selection(QgsRubberBand):

    def __init__(self, canvas, wkbType, parent=None):
        """Constructor."""
        super().__init__(canvas, wkbType)

        self.wkbType = wkbType
        self.canvas = canvas

        self.selectedFeature = None

        self.styleUi()

    def styleUi(self):
        """Style the rubber band."""
        raise NotImplementedError("Selection.styleUi: must be implemented in subclass")

    @pyqtSlot()
    def cleanUp(self):
        """Clean up the selection."""
        self.hide()
        self.reset(self.wkbType)
        self.canvas.scene().removeItem(self)

    @pyqtSlot()
    def clearSelectedFeature(self):
        """Clear the selected feature."""
        self.selectedFeature = None
        self.refreshUi()

    def setSelectedFeature(self, feature):
        """Set the selection."""

        if not isinstance(feature, QgsFeature):
            raise PaddockPowerError(
                "Selection.setSelection: feature must be a QgsFeature object")

        self.selectedFeature = feature
        self.refreshUi()

    def updateGeometry(self, geometry):
        """Set the rubber band to a geometry."""
        self.reset(self.wkbType)

        if geometry is None:
            return

        # self.setToGeometry(geometry, None)
        if self.wkbType == QgsWkbTypes.LineGeometry:
            self.setToGeometry(geometry, None)
        elif self.wkbType == QgsWkbTypes.PolygonGeometry:
            self.setToGeometry(geometry, None)

    def refreshUi(self):
        """Refresh the Fence rubber band."""
        self.updateGeometry(self.selectedFeature.geometry()
                           if self.selectedFeature is not None else None)
