# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ...spatial.features.paddock import Paddock
from .paddock_list_item import PaddockListItem
from .feature_layer_list import FeatureLayerList


class PaddockLayerList(FeatureLayerList):

    @classmethod
    def getFeatureType(cls):
        return Paddock

    def __init__(self, parent=None):
        """Constructor."""

        self._derivedMetricPaddockLayerId = None

        def listItemFactory(paddock):
            return PaddockListItem(paddock, self.derivedMetricPaddockLayer, parent=parent)

        super().__init__(listItemFactory, parent)

    @property
    def derivedMetricPaddockLayer(self):
        """Get the FeatureLayer."""
        return QgsProject.instance().mapLayer(self._derivedMetricPaddockLayerId) if self._derivedMetricPaddockLayerId else None

    @derivedMetricPaddockLayer.setter
    def derivedMetricPaddockLayer(self, derivedMetricPaddockLayer):
        """Set the FeatureLayer."""
        self._derivedMetricPaddockLayerId = derivedMetricPaddockLayer.id() if derivedMetricPaddockLayer else None

   