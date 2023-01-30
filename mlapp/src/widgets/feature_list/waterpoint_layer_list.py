# -*- coding: utf-8 -*-
from ..waterpoint_details.waterpoint_details import WaterpointDetails
from ..waterpoint_details.waterpoint_details_edit import WaterpointDetailsEdit
from .feature_list_item import FeatureListItem
from .feature_layer_list import FeatureLayerList


class WaterpointLayerList(FeatureLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(waterpoint): return FeatureListItem(
            waterpoint,
            detailsWidgetFactory=WaterpointDetails,
            editWidgetFactory=WaterpointDetailsEdit,
            parent=parent)

        super().__init__(listItemFactory, parent)

    @property
    def featureLayer(self):
        """Get the FeatureLayer - override this."""
        return self.workspace.waterpointLayer