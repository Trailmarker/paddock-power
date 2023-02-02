# -*- coding: utf-8 -*-
from ..utils import PLUGIN_NAME
from .features import MetricPaddock
from .derived_metric_paddock_layer import DerivedMetricPaddockLayer
from .metric_paddock_land_types_popup_layer import MetricPaddockCurrentLandTypesPopupLayer, MetricPaddockFutureLandTypesPopupLayer
from .persisted_derived_feature_layer import PersistedDerivedFeatureLayer
from .popup_layer_source_mixin import PopupLayerSourceMixin


class MetricPaddockLayer(PersistedDerivedFeatureLayer, PopupLayerSourceMixin):

    LAYER_NAME = "Metric Paddocks"
    STYLE = "paddock"

    @classmethod
    def getFeatureType(cls):
        return MetricPaddock

    def __init__(self,
                 workspaceFile,
                 *dependentLayers):
        f"""Create a new {PLUGIN_NAME} Paddock Land Types layer."""

        super().__init__(workspaceFile,
                         MetricPaddockLayer.defaultName(),
                         MetricPaddockLayer.defaultStyle(),
                         DerivedMetricPaddockLayer,
                         *dependentLayers)

    @property
    def popupLayerTypes(self):
        return [MetricPaddockCurrentLandTypesPopupLayer, MetricPaddockFutureLandTypesPopupLayer]

    @property
    def relativeLayerPosition(self):
        """Makes the Paddock Land Types popups appear *over* the Paddock layer."""
        return -1
