# -*- coding: utf-8 -*-

from ...utils import PLUGIN_NAME
from ..features.paddock_land_system import PaddockLandSystem
from .derived_paddock_land_systems_layer import DerivedPaddockLandSystemsLayer
from .persisted_derived_feature_layer import PersistedDerivedFeatureLayer


class PaddockLandSystemsLayer(PersistedDerivedFeatureLayer):

    STYLE = "paddock_land_systems_popup"

    def __init__(self, project, gpkgFile, layerName, paddockLayer, landSystemLayer, wateredAreaLayer, conditionTable):
        f"""Create a new {PLUGIN_NAME} Paddock Land Systems layer."""

        derivedPaddockLandSystemsLayer = DerivedPaddockLandSystemsLayer(
            project, f"Derived {layerName}", paddockLayer, landSystemLayer, wateredAreaLayer, conditionTable)

        super().__init__(project, gpkgFile, layerName, derivedPaddockLandSystemsLayer, styleName=PaddockLandSystemsLayer.STYLE)

        self.conditionTable = conditionTable

    def getFeatureType(self):
        return PaddockLandSystem

    def wrapFeature(self, feature):
        return self.getFeatureType()(self, self.conditionTable, feature)
