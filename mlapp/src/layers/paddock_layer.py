# -*- coding: utf-8 -*-
from ..utils import PLUGIN_NAME
from .features import Paddock
from .derived_metric_paddock_layer import DerivedMetricPaddockLayer
from .paddock_land_types_popup_layer import PaddockCurrentLandTypesPopupLayer, PaddockFutureLandTypesPopupLayer
from .persisted_derived_feature_layer import PersistedDerivedFeatureLayer
from .popup_layer_source_mixin import PopupLayerSourceMixin


class PaddockLayer(PersistedDerivedFeatureLayer, PopupLayerSourceMixin):

    LAYER_NAME = "Paddocks"
    STYLE = "paddock"

    @classmethod
    def getFeatureType(cls):
        return Paddock

    def __init__(self,
                 workspaceFile,
                 *dependentLayers):
        f"""Create a new {PLUGIN_NAME} Paddock Land Types layer."""

        super().__init__(workspaceFile,
                         PaddockLayer.defaultName(),
                         PaddockLayer.defaultStyle(),
                         DerivedMetricPaddockLayer,
                         dependentLayers)

    @property
    def popupLayerTypes(self):
        return [PaddockCurrentLandTypesPopupLayer, PaddockFutureLandTypesPopupLayer]

    @property
    def relativeLayerPosition(self):
        """Makes the Paddock Land Types popups appear *over* the Paddock layer."""
        return -1
