# -*- coding: utf-8 -*-
from .feature_mini_list import FeatureMiniList
from .feature_list_item import FeatureListItem
from ..paddock_details.paddock_details import PaddockDetails


class PaddockMiniList(FeatureMiniList):
    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(paddock):
            item = FeatureListItem(paddock, detailsWidgetFactory=PaddockDetails, parent=parent)
            # No editWidgetFactory so editing is turned off
            # Also hide the status controls in the Paddock mini list (PP-67)
            item.hideStatusControls()
            return item

        super().__init__(listItemFactory, parent)
