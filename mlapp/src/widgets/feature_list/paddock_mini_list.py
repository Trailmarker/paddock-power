# -*- coding: utf-8 -*-
from .feature_mini_list import FeatureMiniList
from .persisted_feature_collapsible_list_item import PersistedFeatureCollapsibleListItem
from ..paddock_details.paddock_details import PaddockDetails
from ..paddock_details.paddock_details_edit import PaddockDetailsEdit


class PaddockMiniList(FeatureMiniList):
    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(paddock): return PersistedFeatureCollapsibleListItem(
            paddock, PaddockDetails, PaddockDetailsEdit, parent)

        super().__init__(listItemFactory, parent)
