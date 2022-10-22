# -*- coding: utf-8 -*-
from ...models.state import State

from ..feature_list.feature_layer_list import FeatureLayerList
from ..feature_list.feature_list_item import FeatureListItem


class FenceLayerList(FeatureLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        featureLayer = State().getProject().fenceLayer
        def listItemFactory(fence): return FeatureListItem(fence)

        super().__init__(listItemFactory, featureLayer, parent)
