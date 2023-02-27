# -*- coding: utf-8 -*-
from .feature_layer_list import FeatureLayerList
from .paddock_list_item import PaddockListItem


class PaddockLayerList(FeatureLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(paddock):
            return PaddockListItem(paddock, parent=parent)

        super().__init__(listItemFactory, parent)

        self.featureLayer = self.workspace.paddockLayer
