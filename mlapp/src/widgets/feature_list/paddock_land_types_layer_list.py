# -*- coding: utf-8 -*-
from ..paddock_land_type_details.paddock_land_type_details import PaddockLandSystemDetails
from ..paddock_land_type_details.paddock_land_type_details_edit import PaddockLandSystemDetailsEdit
from .feature_layer_list import FeatureLayerList
from .feature_list_item import FeatureListItem


class PaddockLandSystemsLayerList(FeatureLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(paddockLandSystem):
            paddockLandSystem.featureUpdated.connect(self.refreshUi)
            return FeatureListItem(paddockLandSystem, detailsWidgetFactory=PaddockLandSystemDetails,
                                   editWidgetFactory=PaddockLandSystemDetailsEdit, parent=parent)

        super().__init__(listItemFactory, parent)
