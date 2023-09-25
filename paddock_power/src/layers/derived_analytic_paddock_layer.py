# -*- coding: utf-8 -*-
from ..utils import getSetting, randomString
from .features import AnalyticPaddock
from .fields import ANALYSIS_TYPE, AREA, BUILD_FENCE, FID, NAME, PADDOCK, PERIMETER, STATUS, AnalysisType
from .derived_feature_layer import DerivedFeatureLayer


class DerivedAnalyticPaddockLayer(DerivedFeatureLayer):

    LAYER_NAME = "Derived Analytic Paddocks"
    STYLE = "base_paddock"

    GLITCH_BUFFER = getSetting("glitchBuffer", default=1.0)

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

        _ANALYTIC_PADDOCK_BOUNDARIES = f"AnalyticPaddocksBoundary{randomString()}"
        _INCLUDED_PADDOCKS = f"IncludedPaddocks{randomString()}"

        query = f"""

with
{_ANALYTIC_PADDOCK_BOUNDARIES} as
(select
    st_makepolygon(st_exteriorring("{basePaddocks}".geometry)) as geometry,
    "{basePaddocks}".{FID} as {FID},
    "{basePaddocks}".{FID} as {PADDOCK},
    "{basePaddocks}".{NAME} as {NAME},
    "{basePaddocks}"."{ANALYSIS_TYPE}" as "{ANALYSIS_TYPE}",
    "{basePaddocks}"."{BUILD_FENCE}" as "{BUILD_FENCE}",
    "{basePaddocks}".{STATUS} as {STATUS},
    "{basePaddocks}"."{PERIMETER}" as "{PERIMETER}",
    "{basePaddocks}"."{AREA}" as "{AREA}"
from "{basePaddocks}"
where "{basePaddocks}"."{ANALYSIS_TYPE}" = '{AnalysisType.Default.name}'),
{_INCLUDED_PADDOCKS} as
(select
	"{basePaddocks}".geometry as geometry,
    "{basePaddocks}".{FID} as {FID},
    "{basePaddocks}"."{ANALYSIS_TYPE}" as "{ANALYSIS_TYPE}"
from "{basePaddocks}"
where "{basePaddocks}"."{ANALYSIS_TYPE}" != '{AnalysisType.ExcludePaddock.name}')
select
	st_buffer(st_buffer(st_union({_INCLUDED_PADDOCKS}.geometry), {self.GLITCH_BUFFER}), -{self.GLITCH_BUFFER}) as geometry,
    {_ANALYTIC_PADDOCK_BOUNDARIES}.{FID} as {FID},
    {_ANALYTIC_PADDOCK_BOUNDARIES}.{FID} as {PADDOCK},
    {_ANALYTIC_PADDOCK_BOUNDARIES}.{NAME} as {NAME},
    {_ANALYTIC_PADDOCK_BOUNDARIES}."{ANALYSIS_TYPE}" as "{ANALYSIS_TYPE}",
    {_ANALYTIC_PADDOCK_BOUNDARIES}."{BUILD_FENCE}" as "{BUILD_FENCE}",
    {_ANALYTIC_PADDOCK_BOUNDARIES}.{STATUS} as {STATUS},
    {_ANALYTIC_PADDOCK_BOUNDARIES}."{PERIMETER}" as "{PERIMETER}",
    {_ANALYTIC_PADDOCK_BOUNDARIES}."{AREA}" as "{AREA}"
	from {_ANALYTIC_PADDOCK_BOUNDARIES}
	inner join {_INCLUDED_PADDOCKS}
	on st_contains({_ANALYTIC_PADDOCK_BOUNDARIES}.geometry, {_INCLUDED_PADDOCKS}.geometry)
group by {_ANALYTIC_PADDOCK_BOUNDARIES}.{FID}
"""
# select
#     "{basePaddocks}".geometry as geometry,
#     "{basePaddocks}".{FID} as {FID},
#     "{basePaddocks}".{FID} as {PADDOCK},
#     "{basePaddocks}".{NAME} as {NAME},
#     "{basePaddocks}"."{ANALYSIS_TYPE}" as "{ANALYSIS_TYPE}",
#     "{basePaddocks}"."{BUILD_FENCE}" as "{BUILD_FENCE}",
#     "{basePaddocks}".{STATUS} as {STATUS},
#     "{basePaddocks}"."{PERIMETER}" as "{PERIMETER}",
#     "{basePaddocks}"."{AREA}" as "{AREA}"
# from "{basePaddocks}"
# where "{basePaddocks}"."{ANALYSIS_TYPE}" != '{AnalysisType.ExcludePaddock.name}'

        return super().prepareQuery(query, dependentLayers)

    def __init__(self,
                 dependentLayers,
                 changeset):

        super().__init__(DerivedAnalyticPaddockLayer.defaultName(),
                         DerivedAnalyticPaddockLayer.defaultStyle(),
                         dependentLayers,
                         changeset)
