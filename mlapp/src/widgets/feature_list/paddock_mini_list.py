# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from .feature_mini_list import FeatureMiniList
from .feature_list_item import FeatureListItem
from ..paddock_details.paddock_details import PaddockDetails
from ..paddock_details.paddock_details_edit import PaddockDetailsEdit


class PaddockMiniList(FeatureMiniList):
    def __init__(self, parent=None):
        """Constructor."""

        self._derivedMetricPaddockLayerId = None

        def listItemFactory(paddock):
            return FeatureListItem(paddock, detailsWidgetFactory=(lambda feature: self.makeDetailsWidget(feature)),
                                   editWidgetFactory=PaddockDetailsEdit, parent=parent)

        super().__init__(listItemFactory, parent)

    @property
    def derivedMetricPaddockLayer(self):
        """Get the FeatureLayer."""
        return QgsProject.instance().mapLayer(self._derivedMetricPaddockLayerId) if self._derivedMetricPaddockLayerId else None

    @derivedMetricPaddockLayer.setter
    def derivedMetricPaddockLayer(self, derivedMetricPaddockLayer):
        """Set the FeatureLayer."""
        self._derivedMetricPaddockLayerId = derivedMetricPaddockLayer.id() if derivedMetricPaddockLayer else None

    def makeDetailsWidget(self, feature):
        """Create a new DetailsWidget for the given Feature."""
        detailsWidget = PaddockDetails(feature)
        detailsWidget.derivedMetricPaddockLayer = self.derivedMetricPaddockLayer
        return detailsWidget
