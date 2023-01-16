# -*- coding: utf-8 -*-

from ...utils import PLUGIN_NAME
from ..features.paddock_land_type import PaddockLandSystem
from .derived_paddock_land_types_layer import DerivedPaddockLandSystemsLayer
from .persisted_derived_feature_layer import PersistedDerivedFeatureLayer


class PaddockLandSystemsLayer(PersistedDerivedFeatureLayer):

    STYLE = "paddock_land_types_popup"

    def __init__(self, project, gpkgFile, layerName, paddockLayer, landTypeLayer, wateredAreaLayer, conditionTable):
        f"""Create a new {PLUGIN_NAME} Paddock Land Systems layer."""

        derivedPaddockLandSystemsLayer = DerivedPaddockLandSystemsLayer(
            project, f"Derived {layerName}", paddockLayer, landTypeLayer, wateredAreaLayer, conditionTable)

        super().__init__(project, gpkgFile, layerName, derivedPaddockLandSystemsLayer, styleName=PaddockLandSystemsLayer.STYLE)

        self.conditionTable = conditionTable

    def getFeatureType(self):
        return PaddockLandSystem

    def wrapFeature(self, feature):
        return self.getFeatureType()(self, self.conditionTable, feature)
