# -*- coding: utf-8 -*-

from ..utils import PLUGIN_NAME
from .features import PaddockLandType
from .derived_paddock_land_types_layer import DerivedPaddockLandTypesLayer
from .persisted_derived_feature_layer import PersistedDerivedFeatureLayer


class PaddockLandTypesLayer(PersistedDerivedFeatureLayer):

    LAYER_NAME = "Paddock Land Types"
    STYLE = "paddock_land_types_popup"

    @classmethod
    def getFeatureType(cls):
        return PaddockLandType

    def __init__(self,
                 workspaceFile,
                 *dependentLayers):
        f"""Create a new {PLUGIN_NAME} Paddock Land Types layer."""

        super().__init__(workspaceFile,
                         PaddockLandTypesLayer.defaultName(),
                         PaddockLandTypesLayer.defaultStyle(),
                         DerivedPaddockLandTypesLayer,
                         *dependentLayers)
