# -*- coding: utf-8 -*-
from ...spatial.features.feature_status import FeatureStatus
from .feature_list_base import FeatureListBase


class FeatureLayerList(FeatureListBase):
    def __init__(self, listItemFactory, featureLayer, parent=None):
        """Constructor."""

        super().__init__(listItemFactory, parent)

        self.featureLayer = featureLayer
        self.featureLayer.afterCommitChanges.connect(self.refreshUi)

        self.refreshUi()

    def getFeatures(self):
        """Get the Features."""
        return [feature for feature in self.featureLayer.getFeaturesByStatus(FeatureStatus.Built, FeatureStatus.Drafted, FeatureStatus.Planned)]
