# -*- coding: utf-8 -*-
from ..utils import randomString
from .features import MetricPaddock
from .fields import ANALYSIS_TYPE, AREA, BUILD_FENCE, ESTIMATED_CAPACITY_PER_AREA, ESTIMATED_CAPACITY, FID, NAME, PADDOCK, PERIMETER, POTENTIAL_CAPACITY, POTENTIAL_CAPACITY_PER_AREA, STATUS, TIMEFRAME, WATERED_AREA
from .derived_feature_layer import DerivedFeatureLayer


class DerivedMetricPaddockLayer(DerivedFeatureLayer):

    LAYER_NAME = "Derived Metric Paddocks"
    STYLE = "paddock"

    @classmethod
    def getFeatureType(cls):
        return MetricPaddock

    def getRederiveFeaturesRequest(self):
        """Define which features must be removed from a target layer to be re-derived."""
        if not self.changeset:
            return None

        # TODO Land Type condition table?
        [analyticPaddockLayer, paddockLandTypesLayer] = self.dependentLayers
        return self.prepareRederiveFeaturesRequest(
            analyticPaddockLayer, PADDOCK, FID,
            paddockLandTypesLayer, PADDOCK, PADDOCK)

    def prepareQuery(self, query, dependentLayers):
        [analyticPaddockLayer, paddockLandTypesLayer] = self.dependentLayers
        [analyticPaddocks, paddockLandTypes] = self.names(dependentLayers)

        filterPaddocks = self.andAllKeyClauses(
            self.changeset,
            analyticPaddockLayer,
            FID,
            FID,
            paddockLandTypesLayer,
            FID,
            PADDOCK)

        if filterPaddocks:
            _FILTERED_PADDOCKS = f"FilteredPaddocks{randomString()}"
            withFilteredPaddocks = f"""
with {_FILTERED_PADDOCKS} as
    (select * from "{analyticPaddocks}"
     where 1=1
     {filterPaddocks})
"""
        else:
            _FILTERED_PADDOCKS = analyticPaddocks
            withFilteredPaddocks = ""
        query = f"""
{withFilteredPaddocks}
select
	"{_FILTERED_PADDOCKS}".geometry as geometry,
	"{_FILTERED_PADDOCKS}".{FID} as {FID},
	"{_FILTERED_PADDOCKS}".{FID} as {PADDOCK},
	"{_FILTERED_PADDOCKS}".{NAME} as {NAME},
	"{_FILTERED_PADDOCKS}"."{ANALYSIS_TYPE}" as "{ANALYSIS_TYPE}",
	"{_FILTERED_PADDOCKS}"."{BUILD_FENCE}" as "{BUILD_FENCE}",
	"{_FILTERED_PADDOCKS}".{STATUS} as {STATUS},
    "{paddockLandTypes}".{TIMEFRAME} as {TIMEFRAME},
	"{_FILTERED_PADDOCKS}"."{PERIMETER}" as "{PERIMETER}",
	sum("{paddockLandTypes}"."{AREA}") as "{AREA}",
    sum("{paddockLandTypes}"."{WATERED_AREA}") as "{WATERED_AREA}",
	(sum("{paddockLandTypes}"."{ESTIMATED_CAPACITY}") / nullif("{_FILTERED_PADDOCKS}"."{AREA}", 0.0)) as "{ESTIMATED_CAPACITY_PER_AREA}",
	(sum("{paddockLandTypes}"."{POTENTIAL_CAPACITY}") / nullif("{_FILTERED_PADDOCKS}"."{AREA}", 0.0)) as "{POTENTIAL_CAPACITY_PER_AREA}",
	sum("{paddockLandTypes}"."{ESTIMATED_CAPACITY}") as "{ESTIMATED_CAPACITY}",
	sum("{paddockLandTypes}"."{POTENTIAL_CAPACITY}") as "{POTENTIAL_CAPACITY}"
from "{_FILTERED_PADDOCKS}"
inner join "{paddockLandTypes}"
	on "{_FILTERED_PADDOCKS}".{FID} = "{paddockLandTypes}".{PADDOCK}
group by "{_FILTERED_PADDOCKS}".{FID}, "{paddockLandTypes}".{TIMEFRAME}
"""
        return super().prepareQuery(query, dependentLayers)

    def __init__(self,
                 dependentLayers,
                 changeset):

        super().__init__(DerivedMetricPaddockLayer.defaultName(),
                         DerivedMetricPaddockLayer.defaultStyle(),
                         dependentLayers,
                         changeset)
