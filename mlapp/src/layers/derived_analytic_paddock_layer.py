# -*- coding: utf-8 -*-
from ..utils import randomString
from .features import AnalyticPaddock
from .fields import ANALYSIS_TYPE, AREA, BUILD_FENCE, FID, NAME, PADDOCK, PERIMETER, STATUS, AnalysisType
from .derived_feature_layer import DerivedFeatureLayer


class DerivedAnalyticPaddockLayer(DerivedFeatureLayer):

    LAYER_NAME = "Derived Analytic Paddocks"
    STYLE = "base_paddock"

    @classmethod
    def getFeatureType(cls):
        return AnalyticPaddock

    def getRederiveFeaturesRequest(self):
        """Define which features must be removed from a target layer to be re-derived."""
        return None

        # if not self.changeset:
        #     return None

        # # TODO Land Type condition table?
        # [basePaddockLayer, paddockLandTypesLayer] = self.dependentLayers
        # return self.prepareRederiveFeaturesRequest(
        #     basePaddockLayer, PADDOCK, FID,
        #     paddockLandTypesLayer, PADDOCK, PADDOCK)

    def prepareQuery(self, query, dependentLayers):
        [basePaddockLayer] = self.dependentLayers
        [basePaddocks] = self.names(dependentLayers)

        query = f"""

select
    "{basePaddocks}".geometry as geometry,
    "{basePaddocks}".{FID} as {FID},
    "{basePaddocks}".{FID} as {PADDOCK},
    "{basePaddocks}".{NAME} as {NAME},
    "{basePaddocks}"."{ANALYSIS_TYPE}" as "{ANALYSIS_TYPE}",
    "{basePaddocks}"."{BUILD_FENCE}" as "{BUILD_FENCE}",
    "{basePaddocks}".{STATUS} as {STATUS},
    "{basePaddocks}"."{PERIMETER}" as "{PERIMETER}",
    "{basePaddocks}"."{AREA}" as "{AREA}"
from "{basePaddocks}"
where "{basePaddocks}"."{ANALYSIS_TYPE}" != '{AnalysisType.ExcludePaddock.name}'
"""
        return super().prepareQuery(query, dependentLayers)

    def __init__(self,
                 dependentLayers,
                 changeset):

        super().__init__(DerivedAnalyticPaddockLayer.defaultName(),
                         DerivedAnalyticPaddockLayer.defaultStyle(),
                         dependentLayers,
                         changeset)
