# -*- coding: utf-8 -*-
from ..metric_paddock_details.metric_paddock_details import MetricPaddockDetails
from ..metric_paddock_details.metric_paddock_details_edit import MetricPaddockDetailsEdit
from .feature_list_item import FeatureListItem


class MetricPaddockListItem(FeatureListItem):

    def __init__(self, metricPaddock, parent=None):

        super().__init__(
            metricPaddock,
            detailsWidgetFactory=MetricPaddockDetails,
            editWidgetFactory=self.makeEditWidget,
            parent=parent)

    def makeEditWidget(self, metricPaddock):
        """Create a new edit widget for the given Metric Paddock, that will save edits to the corresponding 'underlying' Paddock."""
        editWidget = MetricPaddockDetailsEdit(metricPaddock)

        return editWidget
