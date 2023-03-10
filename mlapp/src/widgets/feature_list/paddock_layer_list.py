# -*- coding: utf-8 -*-
from .feature_layer_list import FeatureLayerList
from .paddock_list_item import PaddockListItem


class PaddockLayerList(FeatureLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(paddock):
            item = PaddockListItem(paddock, parent=parent)
            # Hide status controls for Paddocks
            item.hideStatusControls()
            return item

        super().__init__(listItemFactory, parent)

        self.featureLayer = self.workspace.paddockLayer
