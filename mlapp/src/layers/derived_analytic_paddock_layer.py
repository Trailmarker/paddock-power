# -*- coding: utf-8 -*-
from ..utils import randomString
from .features import BasePaddock
from .fields import ANALYSIS_TYPE, AREA, BUILD_FENCE, FID, NAME, PERIMETER, STATUS, AnalysisType
from .derived_feature_layer import DerivedFeatureLayer


class DerivedAnalyticPaddockLayer(DerivedFeatureLayer):

    LAYER_NAME = "Derived Analytic Paddocks"
    STYLE = "paddock"

    @classmethod
    def getFeatureType(cls):
        return BasePaddock

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
    "{basePaddocks}".{NAME} as {NAME},
    "{basePaddocks}"."{ANALYSIS_TYPE}" as "{ANALYSIS_TYPE}",
    "{basePaddocks}"."{BUILD_FENCE}" as "{BUILD_FENCE}",
    "{basePaddocks}".{STATUS} as {STATUS},
    "{basePaddocks}"."{PERIMETER}" as "{PERIMETER}",
    "{basePaddocks}"."{AREA}" as "{AREA}"
from "{basePaddocks}"
where "{basePaddocks}"."{ANALYSIS_TYPE}" != '{AnalysisType.ExcludePaddock.name}'
"""
# {withFilteredPaddocks}
# select
# 	"{_FILTERED_PADDOCKS}".geometry as geometry,
# 	"{_FILTERED_PADDOCKS}".{FID} as {FID},
# 	"{_FILTERED_PADDOCKS}".{FID} as {PADDOCK},
# 	"{_FILTERED_PADDOCKS}".{NAME} as {NAME},
# 	"{_FILTERED_PADDOCKS}"."{ANALYSIS_TYPE}" as "{ANALYSIS_TYPE}",
# 	"{_FILTERED_PADDOCKS}"."{BUILD_FENCE}" as "{BUILD_FENCE}",
# 	"{_FILTERED_PADDOCKS}".{STATUS} as {STATUS},
#     "{paddockLandTypes}".{TIMEFRAME} as {TIMEFRAME},
# 	"{_FILTERED_PADDOCKS}"."{PERIMETER}" as "{PERIMETER}",
# 	sum("{paddockLandTypes}"."{AREA}") as "{AREA}",
#     sum("{paddockLandTypes}"."{WATERED_AREA}") as "{WATERED_AREA}",
# 	(sum("{paddockLandTypes}"."{ESTIMATED_CAPACITY}") / nullif("{_FILTERED_PADDOCKS}"."{AREA}", 0.0)) as "{ESTIMATED_CAPACITY_PER_AREA}",
# 	(sum("{paddockLandTypes}"."{POTENTIAL_CAPACITY}") / nullif("{_FILTERED_PADDOCKS}"."{AREA}", 0.0)) as "{POTENTIAL_CAPACITY_PER_AREA}",
# 	sum("{paddockLandTypes}"."{ESTIMATED_CAPACITY}") as "{ESTIMATED_CAPACITY}",
# 	sum("{paddockLandTypes}"."{POTENTIAL_CAPACITY}") as "{POTENTIAL_CAPACITY}"
# from "{_FILTERED_PADDOCKS}"
# inner join "{paddockLandTypes}"
# 	on "{_FILTERED_PADDOCKS}".{FID} = "{paddockLandTypes}".{PADDOCK}
# group by "{_FILTERED_PADDOCKS}".{FID}, "{paddockLandTypes}".{TIMEFRAME}
# """
        return super().prepareQuery(query, dependentLayers)

    def __init__(self,
                 dependentLayers,
                 changeset):

        super().__init__(DerivedAnalyticPaddockLayer.defaultName(),
                         DerivedAnalyticPaddockLayer.defaultStyle(),
                         dependentLayers,
                         changeset)
