# -*- coding: utf-8 -*-
from .feature_layer_list import FeatureLayerList
from .feature_list_item import FeatureListItem


class WaterpointLayerList(FeatureLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(waterpoint): return FeatureListItem(waterpoint)

        super().__init__(listItemFactory, parent)
