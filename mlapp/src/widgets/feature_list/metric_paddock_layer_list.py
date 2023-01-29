# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ...spatial.features.metric_paddock import MetricPaddock
from ...utils import qgsDebug
from .feature_layer_list import FeatureLayerList
from .metric_paddock_list_item import MetricPaddockListItem


class MetricPaddockLayerList(FeatureLayerList):

    @classmethod
    def getFeatureType(cls):
        return MetricPaddock

    def __init__(self, parent=None):
        """Constructor."""

        self._paddockLayerId = None

        def listItemFactory(metricPaddock):
            return MetricPaddockListItem(metricPaddock, self.paddockLayer, parent=parent)

        super().__init__(listItemFactory, parent)

    @property
    def paddockLayer(self):
        """Get the FeatureLayer."""
        return QgsProject.instance().mapLayer(self._paddockLayerId) if self._paddockLayerId else None

    @paddockLayer.setter
    def paddockLayer(self, paddockLayer):
        """Set the FeatureLayer."""
        self._paddockLayerId = paddockLayer.id() if paddockLayer else None

    def changeSelection(self, feature):
        """Change the selection to the specified Feature."""
        qgsDebug(f"MetricPaddockLayerList.changeSelection({feature}) - something supposed to happen with popup layers here?")
        super().changeSelection(feature)
        
        