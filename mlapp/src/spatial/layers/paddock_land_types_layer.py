# -*- coding: utf-8 -*-

from ...utils import PLUGIN_NAME
from ..features.paddock_land_type import PaddockLandType
from .derived_paddock_land_types_layer import DerivedPaddockLandTypesLayer
from .persisted_derived_feature_layer import PersistedDerivedFeatureLayer


class PaddockLandTypesLayer(PersistedDerivedFeatureLayer):

    NAME = "Paddock Land Types"
    STYLE = "paddock_land_types_popup"


    @classmethod
    def getFeatureType(cls):
        return PaddockLandType

    def __init__(self,
                 workspaceFile,
                 derivedPaddockLandTypesLayer: DerivedPaddockLandTypesLayer):
        f"""Create a new {PLUGIN_NAME} Paddock Land Types layer."""

        super().__init__(workspaceFile,
                         layerName=PaddockLandTypesLayer.NAME,
                         styleName=PaddockLandTypesLayer.STYLE,
                         derivedLayer=derivedPaddockLandTypesLayer)
