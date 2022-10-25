# -*- coding: utf-8 -*-
from .feature_collapsible_list_item import FeatureCollapsibleListItem
from .feature_layer_list import FeatureLayerList
from ..paddock_details.paddock_details import PaddockDetails
from ..paddock_details.paddock_details_edit import PaddockDetailsEdit


class PaddockLayerList(FeatureLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(paddock): return FeatureCollapsibleListItem(
            paddock, PaddockDetails, PaddockDetailsEdit, parent)

        super().__init__(listItemFactory, parent)
