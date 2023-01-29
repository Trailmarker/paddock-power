# -*- coding: utf-8 -*-
from .infrastructure_list_item import InfrastructureListItem
from .feature_layer_list import FeatureLayerList


class FenceLayerList(FeatureLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(fence): return InfrastructureListItem(fence, parent=parent)

        super().__init__(listItemFactory, parent)
