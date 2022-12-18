# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSlot

from qgis.core import QgsProject

from .feature_list_base import FeatureListBase


class FeatureLayerList(FeatureListBase):
    def __init__(self, listItemFactory, parent=None):
        """Constructor."""

        super().__init__(listItemFactory, parent)

        self._featureLayerId = None
        self.refreshUi()

    @property
    def featureLayer(self):
        """Get the FeatureLayer."""
        return QgsProject.instance().mapLayer(self._featureLayerId) if self._featureLayerId else None

    @featureLayer.setter
    def featureLayer(self, featureLayer):
        """Set the FeatureLayer."""
        if featureLayer:
            self._featureLayerId = featureLayer.id()
            self.featureLayer.selectedFeatureChanged.connect(self.onSelectedFeatureChanged)
        else:
            self._featureLayerId = None
        self.refreshUi()

    def getFeatures(self):
        """Get the Features."""
        if self.featureLayer:
            return [feature for feature in self.featureLayer.getFeatures()]
        else:
            return []
