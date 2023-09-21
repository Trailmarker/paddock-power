# -*- coding: utf-8 -*-
from qgis.core import QgsFeatureRequest

from .fields import PADDOCK, TIMEFRAME
from ..utils import PLUGIN_NAME
from .features import BasePaddock
from .derived_analytic_paddock_layer import DerivedAnalyticPaddockLayer
from .persisted_derived_feature_layer import PersistedDerivedFeatureLayer


class AnalyticPaddockLayer(PersistedDerivedFeatureLayer):

    LAYER_NAME = "Analytic Paddocks"
    STYLE = "paddock"

    @classmethod
    def getFeatureType(cls):
        return BasePaddock

    def __init__(self,
                 workspaceFile,
                 *dependentLayers):
        f"""Create a new {PLUGIN_NAME} Paddock Land Types layer."""
        PersistedDerivedFeatureLayer.__init__(self,
                                              workspaceFile,
                                              AnalyticPaddockLayer.defaultName(),
                                              AnalyticPaddockLayer.defaultStyle(),
                                              DerivedAnalyticPaddockLayer,
                                              dependentLayers)
