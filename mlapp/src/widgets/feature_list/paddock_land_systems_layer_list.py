# -*- coding: utf-8 -*-
from ...utils import qgsDebug
from ..paddock_land_system_details.paddock_land_system_details import PaddockLandSystemDetails
from ..paddock_land_system_details.paddock_land_system_details_edit import PaddockLandSystemDetailsEdit
from .paddock_land_system_list_item import PaddockLandSystemListItem
from .feature_layer_list import FeatureLayerList


class PaddockLandSystemsLayerList(FeatureLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(paddockLandSystem):
            return PaddockLandSystemListItem(paddockLandSystem, PaddockLandSystemDetails,
                                             PaddockLandSystemDetailsEdit, parent)

        super().__init__(listItemFactory, parent)

    def refreshUi(self):
        """Refresh the UI."""
        qgsDebug(f"Refreshing PaddockLandSystemsLayerList")
        super().refreshUi()
