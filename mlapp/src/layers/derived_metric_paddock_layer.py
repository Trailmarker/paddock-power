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

    def prepareQuery(self, query, *dependentLayers):
        [paddockLayer, paddockLandTypesLayer] = self.names(*dependentLayers)

        query = f"""
select
	"{paddockLayer}".geometry as geometry,
	"{paddockLayer}".{FID} as {FID},
	"{paddockLayer}".{FID} as {PADDOCK},
	"{paddockLayer}".{NAME} as {NAME},
	"{paddockLayer}".{STATUS} as {STATUS},
    "{paddockLandTypesLayer}".{TIMEFRAME} as {TIMEFRAME},
	sum("{paddockLandTypesLayer}"."{AREA}") as "{AREA}",
    sum("{paddockLandTypesLayer}"."{WATERED_AREA}") as "{WATERED_AREA}",
	"{paddockLayer}"."{PERIMETER}" as "{PERIMETER}",
	"{paddockLayer}"."{BUILD_FENCE}" as "{BUILD_FENCE}",
	(sum("{paddockLandTypesLayer}"."{ESTIMATED_CAPACITY}") / nullif("{paddockLayer}"."{AREA}", 0.0)) as "{ESTIMATED_CAPACITY_PER_AREA}",
	sum("{paddockLandTypesLayer}"."{ESTIMATED_CAPACITY}") as "{ESTIMATED_CAPACITY}",
	(sum("{paddockLandTypesLayer}"."{POTENTIAL_CAPACITY}") / nullif("{paddockLayer}"."{AREA}", 0.0)) as "{POTENTIAL_CAPACITY_PER_AREA}",
	sum("{paddockLandTypesLayer}"."{POTENTIAL_CAPACITY}") as "{POTENTIAL_CAPACITY}"
from "{paddockLayer}"
inner join "{paddockLandTypesLayer}"
	on "{paddockLayer}".{FID} = "{paddockLandTypesLayer}".{PADDOCK}
group by "{paddockLayer}".{FID}, "{paddockLandTypesLayer}".{TIMEFRAME}
"""
        return super().prepareQuery(query, *dependentLayers)

    def getFeatureByPaddockId(self, paddockId):
        """Return a MetricPaddock based on a Paddock FID."""
        paddockIdRequest = QgsFeatureRequest().setFilterExpression(f'"{PADDOCK}" = {paddockId}')
        features = [f for f in self.getFeatures(paddockIdRequest)]
        if not features:
            return None
        else:
            for f in features:
                if Timeframe[f.timeframe.name] == Timeframe[self.timeframe.name]:
                    return f

    def __init__(self,
                 paddockLayer,
                 paddockLandTypesLayer):

        super().__init__(DerivedMetricPaddockLayer.defaultName(),
                         DerivedMetricPaddockLayer.defaultStyle(),
                         paddockLayer,
                         paddockLandTypesLayer)
