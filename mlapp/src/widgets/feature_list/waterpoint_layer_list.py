# -*- coding: utf-8 -*-
from ..waterpoint_details.waterpoint_details import WaterpointDetails
from ..waterpoint_details.waterpoint_details_edit import WaterpointDetailsEdit
from .feature_list_item import FeatureListItem
from .persisted_feature_layer_list import PersistedFeatureLayerList


class WaterpointLayerList(PersistedFeatureLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(waterpoint): return FeatureListItem(waterpoint, detailsWidgetFactory=WaterpointDetails, editWidgetFactory=WaterpointDetailsEdit, parent=parent)

        super().__init__(listItemFactory, parent)
