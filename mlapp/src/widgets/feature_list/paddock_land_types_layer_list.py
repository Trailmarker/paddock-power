# -*- coding: utf-8 -*-
from ...utils import qgsDebug
from ...spatial.fields.timeframe import Timeframe
from ...spatial.layers.metric_paddock_land_types_popup_layer import MetricPaddockCurrentLandTypesPopupLayer, MetricPaddockFutureLandTypesPopupLayer
from ..paddock_land_type_details.paddock_land_type_details import PaddockLandTypeDetails
from ..paddock_land_type_details.paddock_land_type_details_edit import PaddockLandTypeDetailsEdit
from .popup_layer_list import PopupLayerList
from .feature_list_item import FeatureListItem


class PaddockLandTypesLayerList(PopupLayerList):

    def __init__(self, parent=None):
        """Constructor."""

        self._featureLayer = None

        def listItemFactory(paddockLandType):
            return FeatureListItem(paddockLandType, detailsWidgetFactory=PaddockLandTypeDetails,
                                   editWidgetFactory=PaddockLandTypeDetailsEdit, noEdits=True, parent=parent)
            

        super().__init__(listItemFactory, parent)

    @property
    def featureLayer(self):
        return self._featureLayer

    @featureLayer.setter
    def featureLayer(self, value):
        self._featureLayer = value
        self.refreshUi()

    def onPopupLayerAdded(self, layer):
        if type(layer) not in self.popupLayerTypes:
            return
        self._featureLayer = layer
        self.refreshUi()

    def onPopupLayerRemoved(self):
        self.featureLayer = None

    def getFeatures(self):
        """Get the current popup layer of the given type."""
        if not self._featureLayer:
            return []
        features = self._featureLayer.getFeaturesByTimeframe(self.timeframe)
        qgsDebug(f"{self.__class__.__name__}.getFeatures: {len(features)} features in {self.timeframe.name} timeframe")
        return features


class CurrentPaddockLandTypesLayerList(PaddockLandTypesLayerList):
    """A popup layer consumer list for collections of PaddockLandTypes
    in the Current timeframe only."""

    def __init__(self, parent=None):
        super().__init__(parent)

    @property
    def popupLayerType(self):
        return MetricPaddockCurrentLandTypesPopupLayer

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
        return MetricPaddockFutureLandTypesPopupLayer

    @property
    def timeframe(self):
        return Timeframe.Future
