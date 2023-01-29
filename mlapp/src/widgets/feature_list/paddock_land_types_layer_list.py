# -*- coding: utf-8 -*-
from ..paddock_land_type_details.paddock_land_type_details import PaddockLandTypeDetails
from ..paddock_land_type_details.paddock_land_type_details_edit import PaddockLandTypeDetailsEdit
from .feature_layer_list import FeatureLayerList
from .feature_list_item import FeatureListItem


class PaddockLandTypesLayerList(FeatureLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(paddockLandType):
            return FeatureListItem(paddockLandType, detailsWidgetFactory=PaddockLandTypeDetails,
                                   editWidgetFactory=PaddockLandTypeDetailsEdit, parent=parent)

        super().__init__(listItemFactory, parent)
