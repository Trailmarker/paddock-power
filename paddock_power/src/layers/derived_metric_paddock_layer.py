# -*- coding: utf-8 -*-
from ..utils import randomString
from .features import MetricPaddock
from .fields import AnalysisType, Timeframe, ANALYSIS_TYPE, AREA, BUILD_FENCE, ESTIMATED_CAPACITY_PER_AREA, ESTIMATED_CAPACITY, FID, NAME, PADDOCK, PERIMETER, POTENTIAL_CAPACITY, POTENTIAL_CAPACITY_PER_AREA, STATUS, TIMEFRAME, WATERED_AREA
from .derived_feature_layer import DerivedFeatureLayer


class DerivedMetricPaddockLayer(DerivedFeatureLayer):

    LAYER_NAME = "Derived Metric Paddocks"
    STYLE = "paddock"

    @classmethod
    def getFeatureType(cls):
        return MetricPaddock

    def getRederiveFeaturesRequest(self):
        """Define which features must be removed from a target layer to be re-derived."""
        if self.changeset.isEmpty:
            return None

        # TODO Land Type condition table?
        [basePaddockLayer, analyticPaddockLayer, paddockLandTypesLayer] = self.dependentLayers
        return self.prepareRederiveFeaturesRequest(
            basePaddockLayer, PADDOCK, FID,
            analyticPaddockLayer, PADDOCK, PADDOCK,
            paddockLandTypesLayer, PADDOCK, PADDOCK)

    def prepareQuery(self, query, dependentLayers):
        [basePaddockLayer, analyticPaddockLayer, paddockLandTypesLayer] = self.dependentLayers
        [basePaddocks, analyticPaddocks, paddockLandTypes] = self.names(dependentLayers)

        filterPaddocks = self.andAllKeyClauses(
            self.changeset,
            basePaddockLayer,
            FID,
            FID,
            analyticPaddockLayer,
            FID,
            FID,
            paddockLandTypesLayer,
            FID,
            PADDOCK)

        _ANALYTIC_PADDOCKS = f"AnalyticPaddocks{randomString()}"
        _OTHER_PADDOCKS = f"OtherPaddocks{randomString()}"

        withAnalyticPaddocks = f"""
    {_ANALYTIC_PADDOCKS} as
    (select * from "{analyticPaddocks}"
     where 1=1
     {filterPaddocks})
"""
        withOtherPaddocks = f"""
    {_OTHER_PADDOCKS} as
    (select * from "{basePaddocks}"
    where "{basePaddocks}"."{ANALYSIS_TYPE}" != '{AnalysisType.Default.name}')
"""
        query = f"""
with
{withAnalyticPaddocks},
{withOtherPaddocks}
select
	"{_ANALYTIC_PADDOCKS}".geometry as geometry,
	"{_ANALYTIC_PADDOCKS}".{FID} as {FID},
	"{_ANALYTIC_PADDOCKS}".{PADDOCK} as {PADDOCK},
	"{_ANALYTIC_PADDOCKS}".{NAME} as {NAME},
	"{_ANALYTIC_PADDOCKS}"."{ANALYSIS_TYPE}" as "{ANALYSIS_TYPE}",
	"{_ANALYTIC_PADDOCKS}"."{BUILD_FENCE}" as "{BUILD_FENCE}",
	"{_ANALYTIC_PADDOCKS}".{STATUS} as {STATUS},
    "{paddockLandTypes}".{TIMEFRAME} as {TIMEFRAME},
	"{_ANALYTIC_PADDOCKS}"."{PERIMETER}" as "{PERIMETER}",
	sum("{paddockLandTypes}"."{AREA}") as "{AREA}",
    sum("{paddockLandTypes}"."{WATERED_AREA}") as "{WATERED_AREA}",
	(sum("{paddockLandTypes}"."{ESTIMATED_CAPACITY}") / nullif("{_ANALYTIC_PADDOCKS}"."{AREA}", 0.0)) as "{ESTIMATED_CAPACITY_PER_AREA}",
	(sum("{paddockLandTypes}"."{POTENTIAL_CAPACITY}") / nullif("{_ANALYTIC_PADDOCKS}"."{AREA}", 0.0)) as "{POTENTIAL_CAPACITY_PER_AREA}",
	sum("{paddockLandTypes}"."{ESTIMATED_CAPACITY}") as "{ESTIMATED_CAPACITY}",
	sum("{paddockLandTypes}"."{POTENTIAL_CAPACITY}") as "{POTENTIAL_CAPACITY}"
from "{_ANALYTIC_PADDOCKS}"
inner join "{paddockLandTypes}"
	on "{_ANALYTIC_PADDOCKS}".{PADDOCK} = "{paddockLandTypes}".{PADDOCK}
group by "{_ANALYTIC_PADDOCKS}".{FID}, "{paddockLandTypes}".{TIMEFRAME}
union
select
	"{_OTHER_PADDOCKS}".geometry as geometry,
	"{_OTHER_PADDOCKS}".{FID} as {FID},
	"{_OTHER_PADDOCKS}".{FID} as {PADDOCK},
	"{_OTHER_PADDOCKS}".{NAME} as {NAME},
	"{_OTHER_PADDOCKS}"."{ANALYSIS_TYPE}" as "{ANALYSIS_TYPE}",
	"{_OTHER_PADDOCKS}"."{BUILD_FENCE}" as "{BUILD_FENCE}",
	"{_OTHER_PADDOCKS}".{STATUS} as {STATUS},
    '{Timeframe.Current.name}' as {TIMEFRAME},
	"{_OTHER_PADDOCKS}"."{PERIMETER}" as "{PERIMETER}",
    "{_OTHER_PADDOCKS}"."{AREA}" as "{AREA}",
    0.0 as "{WATERED_AREA}",
    0.0 as "{ESTIMATED_CAPACITY_PER_AREA}",
    0.0 as "{POTENTIAL_CAPACITY_PER_AREA}",
    0.0 as "{ESTIMATED_CAPACITY}",
    0.0 as "{POTENTIAL_CAPACITY}"
from "{_OTHER_PADDOCKS}"
union
select
	"{_OTHER_PADDOCKS}".geometry as geometry,
	"{_OTHER_PADDOCKS}".{FID} as {FID},
	"{_OTHER_PADDOCKS}".{FID} as {PADDOCK},
	"{_OTHER_PADDOCKS}".{NAME} as {NAME},
	"{_OTHER_PADDOCKS}"."{ANALYSIS_TYPE}" as "{ANALYSIS_TYPE}",
	"{_OTHER_PADDOCKS}"."{BUILD_FENCE}" as "{BUILD_FENCE}",
	"{_OTHER_PADDOCKS}".{STATUS} as {STATUS},
    '{Timeframe.Future.name}' as {TIMEFRAME},
	"{_OTHER_PADDOCKS}"."{PERIMETER}" as "{PERIMETER}",
    "{_OTHER_PADDOCKS}"."{AREA}" as "{AREA}",
    0.0 as "{WATERED_AREA}",
    0.0 as "{ESTIMATED_CAPACITY_PER_AREA}",
    0.0 as "{POTENTIAL_CAPACITY_PER_AREA}",
    0.0 as "{ESTIMATED_CAPACITY}",
    0.0 as "{POTENTIAL_CAPACITY}"
from "{_OTHER_PADDOCKS}"
"""
        return super().prepareQuery(query, dependentLayers)

    def __init__(self,
                 dependentLayers,
                 changeset):

        super().__init__(DerivedMetricPaddockLayer.defaultName(),
                         DerivedMetricPaddockLayer.defaultStyle(),
                         dependentLayers,
                         changeset)
