# -*- coding: utf-8 -*-
from ..utils import PLUGIN_NAME
from .features import AnalyticPaddock
from .derived_analytic_paddock_layer import DerivedAnalyticPaddockLayer
from .persisted_derived_feature_layer import PersistedDerivedFeatureLayer


class AnalyticPaddockLayer(PersistedDerivedFeatureLayer):

    LAYER_NAME = "Analytic Paddocks"
    STYLE = "base_paddock"

    @classmethod
    def getFeatureType(cls):
        return AnalyticPaddock

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
