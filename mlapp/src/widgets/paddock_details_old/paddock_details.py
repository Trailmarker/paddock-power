# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

from qgis.core import QgsProject

from ...models import WorkspaceMixin

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'paddock_details_base.ui')))


class PaddockDetails(QWidget, FORM_CLASS, WorkspaceMixin):

    def __init__(self, paddock, parent=None):
        """Constructor."""
        QWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)
        WorkspaceMixin.__init__(self)

        self.setupUi(self)

        self.paddock = paddock
        self.metricPaddock = None

        self.refreshUi()

    @property
    def featureLayer(self):
        """Get the FeatureLayer."""
        return self.workspace.paddockLayer

    def refreshUi(self):
        """Set the FeatureLayer and update the display."""

        if self.featureLayer and self.paddock:
            self.metricPaddock = self.featureLayer.getFeatureByPaddockId(self.paddock.FID)

            if self.metricPaddock is not None:
                self.areaText.setValue(self.metricPaddock.AREA, "{0:.2f}")
                self.wateredAreaText.setValue(self.metricPaddock.WATERED_AREA, "{0:.2f}")
                self.perimeterText.setValue(self.metricPaddock.PERIMETER, "{0:.1f}")
                self.estimatedCapacityText.setValue(self.metricPaddock.ESTIMATED_CAPACITY, "{0:.0f}")
                self.potentialCapacityText.setValue(self.metricPaddock.POTENTIAL_CAPACITY, "{0:.0f}")
                self.estimatedCapacityPerAreaText.setValue(self.metricPaddock.ESTIMATED_CAPACITY_PER_AREA, "{0:.1f}")
                self.wateredAreaText.setValue(self.metricPaddock.WATERED_AREA, "{0:.2f}")
                # self.potentialCapacityPerAreaText.setValue(self.metricPaddock.potentialCapacityPerArea, "{0:.1f}")
