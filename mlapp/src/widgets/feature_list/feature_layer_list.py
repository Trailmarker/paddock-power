# -*- coding: utf-8 -*-
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
        """Set the Project."""
        self._featureLayerId = featureLayer.id() if featureLayer else None
        self.featureLayer.editsPersisted.connect(self.refreshUi)
        self.refreshUi()

    def getFeatures(self):
        """Get the Features."""
        if self.featureLayer:
            return [feature for feature in self.featureLayer.getFeaturesByStatus(*self.featureLayer.displayFilter)]
        else:
            return []
