# -*- coding: utf-8 -*-
from mlapp.src.utils import qgsDebug
from .feature_list_base import FeatureListBase


class FeatureLayerList(FeatureListBase):
    def __init__(self, listItemFactory, featureLayer, parent=None):
        """Constructor."""

        super().__init__(listItemFactory, parent)

        self.featureLayer = featureLayer

        # TODO disable the list while the featureLayer is being edited?
        # self.featureLayer.beforeEditingStarted.connect(self.refreshUi)
        self.featureLayer.afterCommitChanges.connect(self.refreshUi)
        self.featureLayer.displayFilterChanged.connect(self.onDisplayFilterChanged)

        self.refreshUi()

    def onDisplayFilterChanged(self, filter):
        qgsDebug(f"FeatureLayerList.onDisplayFilterChanged: {str(filter)}")
        self.refreshUi()

    def getFeatures(self):
        """Get the Features."""
        return [feature for feature in self.featureLayer.getFeaturesByStatus(*self.featureLayer.displayFilter)]
