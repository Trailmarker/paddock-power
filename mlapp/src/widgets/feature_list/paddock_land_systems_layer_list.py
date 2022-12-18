# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ...utils import qgsDebug
from ..paddock_land_system_details.paddock_land_system_details import PaddockLandSystemDetails
from ..paddock_land_system_details.paddock_land_system_details_edit import PaddockLandSystemDetailsEdit
from .feature_collapsible_list_item import FeatureCollapsibleListItem
from .feature_layer_list import FeatureLayerList


class PaddockLandSystemsLayerList(FeatureLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(condition):
            return FeatureCollapsibleListItem(condition, PaddockLandSystemDetails, PaddockLandSystemDetailsEdit, parent)

        super().__init__(listItemFactory, parent)

    def refreshUi(self):
        """Refresh the UI."""
        qgsDebug(f"Refreshing PaddockLandSystemsLayerList")
        # super().refreshUi()
