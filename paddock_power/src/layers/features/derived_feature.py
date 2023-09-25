# -*- coding: utf-8 -*-
from .persisted_feature import PersistedFeature


class DerivedFeature(PersistedFeature):

    def __init__(self, featureLayer, existingFeature=None):
        """Create a new Feature."""

        super().__init__(featureLayer, existingFeature)

    def recalculate(self):
        """Nothing should be recalculated for our derived features."""
        pass
