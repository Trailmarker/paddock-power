# -*- coding: utf-8 -*-

from .feature_layer_list import FeatureLayerList
from .metric_paddock_list_item import MetricPaddockListItem


class MetricPaddockLayerList(FeatureLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(metricPaddock):
            return MetricPaddockListItem(metricPaddock, parent=parent)

        super().__init__(listItemFactory, parent)

    @property
    def featureLayer(self):
        """Get the FeatureLayer - override this."""
        return self.workspace.derivedMetricPaddockLayer
