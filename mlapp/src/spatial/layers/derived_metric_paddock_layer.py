# -*- coding: utf-8 -*-
from qgis.core import QgsFeatureRequest, QgsProject

from ..features.metric_paddock import MetricPaddock
from ..fields.names import AREA, BUILD_FENCE, ESTIMATED_CAPACITY_PER_AREA, ESTIMATED_CAPACITY, FID, NAME, PADDOCK, PERIMETER, POTENTIAL_CAPACITY, POTENTIAL_CAPACITY_PER_AREA, STATUS, TIMEFRAME, WATERED_AREA
from ..fields.timeframe import Timeframe
from .derived_feature_layer import DerivedFeatureLayer


class DerivedMetricPaddockLayer(DerivedFeatureLayer):

    STYLE = "paddock"

    def parameteriseQuery(self, PaddockLayer, PaddockLandTypesLayer):
        return f"""
select
	"{PaddockLayer}".geometry as geometry,
	"{PaddockLayer}".{FID} as {FID},
	"{PaddockLayer}".{FID} as {PADDOCK},
	"{PaddockLayer}".{NAME} as {NAME},
	"{PaddockLayer}".{STATUS} as {STATUS},
    "{PaddockLandTypesLayer}".{TIMEFRAME} as {TIMEFRAME},
	sum("{PaddockLandTypesLayer}"."{AREA}") as "{AREA}",
    sum("{PaddockLandTypesLayer}"."{WATERED_AREA}") as "{WATERED_AREA}",
	"{PaddockLayer}"."{PERIMETER}" as "{PERIMETER}",
	"{PaddockLayer}"."{BUILD_FENCE}" as "{BUILD_FENCE}",
	(sum("{PaddockLandTypesLayer}"."{ESTIMATED_CAPACITY}") / nullif("{PaddockLayer}"."{AREA}", 0.0)) as "{ESTIMATED_CAPACITY_PER_AREA}",
	sum("{PaddockLandTypesLayer}"."{ESTIMATED_CAPACITY}") as "{ESTIMATED_CAPACITY}",
	(sum("{PaddockLandTypesLayer}"."{POTENTIAL_CAPACITY}") / nullif("{PaddockLayer}"."{AREA}", 0.0)) as "{POTENTIAL_CAPACITY_PER_AREA}",
	sum("{PaddockLandTypesLayer}"."{POTENTIAL_CAPACITY}") as "{POTENTIAL_CAPACITY}"
from "{PaddockLayer}"
inner join "{PaddockLandTypesLayer}"
	on "{PaddockLayer}".{FID} = "{PaddockLandTypesLayer}".{PADDOCK}
group by "{PaddockLayer}".{FID}, "{PaddockLandTypesLayer}".{TIMEFRAME}
"""

    def getFeatureType(self):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return MetricPaddock

    def getFeatureByPaddockId(self, paddockId):
        """Return a MetricPaddock based on a Paddock FID."""
        paddockIdRequest = QgsFeatureRequest().setFilterExpression(f'"{PADDOCK}" = {paddockId}')
        features = [f for f in self.getFeatures(paddockIdRequest)]
        if not features:
            return None
        else:
            for f in features:
                if Timeframe[f.timeframe.name] == Timeframe[self.getPaddockPowerProject().currentTimeframe.name]:
                    return f 
    
       
    def __init__(self, project, layerName, paddockLayer, paddockLandTypesLayer, conditionTable):

        super().__init__(
            project,
            layerName,
            self.parameteriseQuery(paddockLayer.name(), paddockLandTypesLayer.name()),
            DerivedMetricPaddockLayer.STYLE,
            paddockLayer,
            paddockLandTypesLayer)
        
        self._paddockLayerId = paddockLayer.id()
        self._paddockLandTypesLayerId = paddockLandTypesLayer.id()
        self.conditionTable = conditionTable

    @property
    def paddockLayer(self):
        return QgsProject.instance().mapLayer(self._paddockLayerId)
        
    @property
    def paddockLandTypesLayer(self):
        return QgsProject.instance().mapLayer(self._paddockLandTypesLayerId)

    def wrapFeature(self, feature):
        # Burn in the FID that gets generated by QGIS for consistency
        feature.setAttribute(FID, feature.id())
        return MetricPaddock(self, self.paddockLayer, self.paddockLandTypesLayer, self.conditionTable, feature)
