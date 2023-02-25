# -*- coding: utf-8 -*-
from qgis.core import QgsFeatureRequest

from .features import MetricPaddock
from .fields import AREA, BUILD_FENCE, ESTIMATED_CAPACITY_PER_AREA, ESTIMATED_CAPACITY, FID, NAME, PADDOCK, PERIMETER, POTENTIAL_CAPACITY, POTENTIAL_CAPACITY_PER_AREA, STATUS, TIMEFRAME, WATERED_AREA, Timeframe
from .derived_feature_layer import DerivedFeatureLayer


class DerivedMetricPaddockLayer(DerivedFeatureLayer):

    LAYER_NAME = "Derived Metric Paddocks"
    STYLE = "paddock"

    @classmethod
    def getFeatureType(cls):
        return MetricPaddock

    def prepareQuery(self, query, dependentLayers):
        [basePaddockLayer, paddockLandTypesLayer] = self.names(dependentLayers)

        query = f"""
select
	"{basePaddockLayer}".geometry as geometry,
	"{basePaddockLayer}".{FID} as {FID},
	"{basePaddockLayer}".{FID} as {PADDOCK},
	"{basePaddockLayer}".{NAME} as {NAME},
	"{basePaddockLayer}"."{BUILD_FENCE}" as "{BUILD_FENCE}",
	"{basePaddockLayer}".{STATUS} as {STATUS},
    "{paddockLandTypesLayer}".{TIMEFRAME} as {TIMEFRAME},
	"{basePaddockLayer}"."{PERIMETER}" as "{PERIMETER}",
	sum("{paddockLandTypesLayer}"."{AREA}") as "{AREA}",
    sum("{paddockLandTypesLayer}"."{WATERED_AREA}") as "{WATERED_AREA}",
	(sum("{paddockLandTypesLayer}"."{ESTIMATED_CAPACITY}") / nullif("{basePaddockLayer}"."{AREA}", 0.0)) as "{ESTIMATED_CAPACITY_PER_AREA}",
	sum("{paddockLandTypesLayer}"."{ESTIMATED_CAPACITY}") as "{ESTIMATED_CAPACITY}",
	(sum("{paddockLandTypesLayer}"."{POTENTIAL_CAPACITY}") / nullif("{basePaddockLayer}"."{AREA}", 0.0)) as "{POTENTIAL_CAPACITY_PER_AREA}",
	sum("{paddockLandTypesLayer}"."{POTENTIAL_CAPACITY}") as "{POTENTIAL_CAPACITY}"
from "{basePaddockLayer}"
inner join "{paddockLandTypesLayer}"
	on "{basePaddockLayer}".{FID} = "{paddockLandTypesLayer}".{PADDOCK}
group by "{basePaddockLayer}".{FID}, "{paddockLandTypesLayer}".{TIMEFRAME}
"""
        return super().prepareQuery(query, dependentLayers)

    def __init__(self,
                 dependentLayers,
                 edits):

        super().__init__(DerivedMetricPaddockLayer.defaultName(),
                         DerivedMetricPaddockLayer.defaultStyle(),
                         dependentLayers,
                         None) # Don't try to get fancy
