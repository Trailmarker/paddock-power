# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSlot

from qgis.core import QgsWkbTypes
from qgis.gui import QgsRubberBand

from ..models.glitch import Glitch
from .features.persisted_feature import PersistedFeature


class Selection(QgsRubberBand):

    def __init__(self, project, canvas, wkbType):
        """Constructor."""
        super().__init__(canvas, wkbType)

        project.selectedFeatureChanged.connect(self.setSelectedFeature)
        self.canvas = canvas
        self.wkbType = wkbType

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

    @pyqtSlot(PersistedFeature)
    def setSelectedFeature(self, feature):
        """Set the selection."""

        if not isinstance(feature, PersistedFeature):
            raise Glitch(
                "Your selected feature must be a Paddock Power Feature.")

        self.selectedFeature = feature
        self.refreshUi()

    def updateGeometry(self, geometry):
        """Set the rubber band to a geometry."""
        self.reset(self.wkbType)

        if geometry is None:
            return

        if self.wkbType == QgsWkbTypes.LineGeometry:
            self.setToGeometry(geometry, None)
        elif self.wkbType == QgsWkbTypes.PolygonGeometry:
            self.setToGeometry(geometry, None)

    def refreshUi(self):
        """Refresh the Fence rubber band."""
        self.updateGeometry(self.selectedFeature.geometry
                            if self.selectedFeature is not None else None)
