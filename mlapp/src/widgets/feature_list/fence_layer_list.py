# -*- coding: utf-8 -*-
from .feature_layer_list import FeatureLayerList
from .feature_list_item import FeatureListItem


class FenceLayerList(FeatureLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(fence): return FeatureListItem(fence)

        super().__init__(listItemFactory, parent)

    
