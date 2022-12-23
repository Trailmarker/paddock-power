# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ..paddock_details.paddock_details import PaddockDetails
from ..paddock_details.paddock_details_edit import PaddockDetailsEdit
from .feature_list_item import FeatureListItem


class PaddockListItem(FeatureListItem):

    def __init__(self, feature, derivedMetricPaddockLayer, parent=None):

        self._derivedMetricPaddockLayerId = derivedMetricPaddockLayer.id()

        super().__init__(feature, detailsWidgetFactory=self.makeDetailsWidget, editWidgetFactory=PaddockDetailsEdit, parent=parent)

    @property
    def derivedMetricPaddockLayer(self):
        """Get the FeatureLayer."""
        return QgsProject.instance().mapLayer(self._derivedMetricPaddockLayerId) if self._derivedMetricPaddockLayerId else None

    def makeDetailsWidget(self, feature):
        """Create a new DetailsWidget for the given Feature."""
        detailsWidget = PaddockDetails(feature)
        detailsWidget.derivedMetricPaddockLayer = self.derivedMetricPaddockLayer
        return detailsWidget
