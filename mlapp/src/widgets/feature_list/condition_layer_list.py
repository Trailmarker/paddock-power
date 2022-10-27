# -*- coding: utf-8 -*-
from .feature_collapsible_list_item import FeatureCollapsibleListItem
from .feature_layer_list import FeatureLayerList
from ..condition_details.condition_details import ConditionDetails
from ..condition_details.condition_details_edit import ConditionDetailsEdit


class ConditionLayerList(FeatureLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(condition):
            return FeatureCollapsibleListItem(condition, ConditionDetails, ConditionDetailsEdit, parent)

        super().__init__(listItemFactory, parent)
