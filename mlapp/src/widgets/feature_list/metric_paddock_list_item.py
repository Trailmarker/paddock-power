# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ..metric_paddock_details.metric_paddock_details import MetricPaddockDetails
from ..metric_paddock_details.metric_paddock_details_edit import MetricPaddockDetailsEdit
from .feature_list_item import FeatureListItem


class MetricPaddockListItem(FeatureListItem):

    def __init__(self, metricPaddock, paddockLayer, parent=None):

        self._paddockLayerId = paddockLayer.id()

        super().__init__(metricPaddock, detailsWidgetFactory=MetricPaddockDetails, editWidgetFactory=self.makeEditWidget, parent=parent)

    @property
    def paddockLayer(self):
        """Get the FeatureLayer."""
        return QgsProject.instance().mapLayer(self._paddockLayerId) if self._paddockLayerId else None

    def makeEditWidget(self, metricPaddock):
        """Create a new edit widget for the given Metric Paddock, that will save edits to the corresponding 'underlying' Paddock."""
        editWidget = MetricPaddockDetailsEdit(metricPaddock)
        editWidget.paddockLayer = self.paddockLayer
        return editWidget
