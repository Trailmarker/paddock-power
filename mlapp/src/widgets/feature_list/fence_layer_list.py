# -*- coding: utf-8 -*-
from .feature_list_item import FeatureListItem
from .persisted_feature_layer_list import PersistedFeatureLayerList

class FenceLayerList(PersistedFeatureLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(fence): return FeatureListItem(fence)

        super().__init__(listItemFactory, parent)
