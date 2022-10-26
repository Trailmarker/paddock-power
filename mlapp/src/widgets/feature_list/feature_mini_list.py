# -*- coding: utf-8 -*-
from ...models.glitch import Glitch
from ...spatial.features.persisted_feature import PersistedFeature
from .feature_list_base import FeatureListBase


class FeatureMiniList(FeatureListBase):
    def __init__(self, listItemFactory, parent=None):
        """Constructor."""
        super().__init__(listItemFactory, parent)
        self.features = []

    def getFeatures(self):
        """Get the paddocks."""
        return self.features

    def setFeatures(self, features):
        """Set the paddocks."""
        if not features:
            self.features = []
        elif not isinstance(features, list) or not all(isinstance(feature, PersistedFeature) for feature in features):
            raise Glitch(
                "The content passed to a Feature mini-list should be a list of Features")
        else:
            self.features = features
        self.refreshUi()
