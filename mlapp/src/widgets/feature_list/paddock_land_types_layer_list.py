# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ...utils import qgsDebug
from ...layers.fields import Timeframe
from ...layers.paddock_land_types_popup_layer import PaddockCurrentLandTypesPopupLayer, PaddockFutureLandTypesPopupLayer
from ..paddock_land_type_details.paddock_land_type_details import PaddockLandTypeDetails
from ..paddock_land_type_details.paddock_land_type_details_edit import PaddockLandTypeDetailsEdit
from .popup_layer_list import PopupLayerList
from .feature_list_item import FeatureListItem


class PaddockLandTypesLayerList(PopupLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        def listItemFactory(paddockLandType):
            return FeatureListItem(paddockLandType, detailsWidgetFactory=PaddockLandTypeDetails,
                                   editWidgetFactory=PaddockLandTypeDetailsEdit, parent=parent)

        super().__init__(listItemFactory, parent)

    def getFeatures(self, request=None):
        """Get the current popup layer of the given type."""
        if not self._featureLayer:
            return []
        features = self._featureLayer.getFeaturesByTimeframe(self.timeframe, request)
        return features


class CurrentPaddockLandTypesLayerList(PaddockLandTypesLayerList):
    """A popup layer consumer list for collections of PaddockLandTypes
    in the Current timeframe only."""

    def __init__(self, parent=None):
        super().__init__(parent)

    @property
    def popupLayerType(self):
        return PaddockCurrentLandTypesPopupLayer

    @property
    def timeframe(self):
        return Timeframe.Current


class FuturePaddockLandTypesLayerList(PaddockLandTypesLayerList):
    """A popup layer consumer list for collections of PaddockLandTypes
    in the Future timeframe only."""

    def __init__(self, parent=None):
        super().__init__(parent)

    @property
    def popupLayerType(self):
        return PaddockFutureLandTypesPopupLayer

    @property
    def timeframe(self):
        return Timeframe.Future
