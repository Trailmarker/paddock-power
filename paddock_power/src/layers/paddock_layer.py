# -*- coding: utf-8 -*-
from qgis.core import QgsFeatureRequest

from ..layers.fields import PADDOCK, TIMEFRAME
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
        PersistedDerivedFeatureLayer.__init__(self,
                                              workspaceFile,
                                              PaddockLayer.defaultName(),
                                              PaddockLayer.defaultStyle(),
                                              DerivedMetricPaddockLayer,
                                              dependentLayers)

        PopupLayerSourceMixin.__init__(self)
        self.connectPopups()

    def getByPaddockId(self, timeframe, paddockId):
        return next(self.getFeatures(QgsFeatureRequest().setFilterExpression(
            f'"{PADDOCK}" = {paddockId} and "{TIMEFRAME}" = \'{timeframe.name}\'')), None)

    def getAnalyticPaddocks(self):
        """Get all Paddock features which are not excluded from analysis."""
        return [f for f in self.getFeatures() if f.isAnalytic]

    @property
    def hasPopups(self):
        return True

    @property
    def popupLayerTypes(self):
        return [PaddockCurrentLandTypesPopupLayer, PaddockFutureLandTypesPopupLayer]

    @property
    def relativeLayerPosition(self):
        """Makes the Paddock Land Types popups appear *over* the Paddock layer."""
        return -1

    @property
    def zoomPopupLayerOnLoad(self):
        """False for this because we're already zoomed to the relevant Paddock."""
        return False
