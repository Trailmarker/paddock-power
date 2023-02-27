# -*- coding: utf-8 -*-
from ...layers.interfaces import IFeature
from ...models import Glitch
from .feature_list_base import FeatureListBase


class FeatureMiniList(FeatureListBase):
    """A flexible mini list of features (doesn't load from a changing source or anything)."""

    def __init__(self, listItemFactory, parent=None):
        """Constructor."""
        super().__init__(listItemFactory, parent)
        self.features = []

    def listFeatures(self):
        """Get the features."""
        return self.features

    def getFeature(self, fid):
        """Get a feature by its fid."""
        for feature in self.features:
            if feature.FID == fid:
                return feature
        return None

    def setFeatures(self, features):
        """Set the paddocks."""
        if not features:
            self.features = []
        elif not isinstance(features, list) or not all(isinstance(feature, IFeature) for feature in features):
            raise Glitch(
                "The content passed to a Feature mini-list should be a list of Features")
        else:
            self.features = features
        self.refreshList()
