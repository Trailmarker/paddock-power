# -*- coding: utf-8 -*-
from ..utils import randomString
from .features import Property
from .fields import AREA, ESTIMATED_CAPACITY, ESTIMATED_CAPACITY_PER_AREA, FID, PERIMETER, POTENTIAL_CAPACITY, POTENTIAL_CAPACITY_PER_AREA, STATUS, TIMEFRAME, WATERED_AREA, Timeframe
from .derived_feature_layer import DerivedFeatureLayer


class DerivedPropertyLayer(DerivedFeatureLayer):

    LAYER_NAME = "Derived Property"
    STYLE = "property"

    @classmethod
    def getFeatureType(cls):
        return Property

    def prepareQuery(self, query, dependentLayers):
        [paddocks] = self.names(dependentLayers)

        # _PROPERTY_TIMEFRAMES = f"PropertyTimeframes{randomString()}"

        query = f"""
select
    st_union(geometry) as geometry,
    0 as {FID},
    "{paddocks}".{TIMEFRAME} as {TIMEFRAME},
    "{paddocks}"."{PERIMETER}" as "{PERIMETER}",
	sum("{paddocks}"."{AREA}") as "{AREA}",
    sum("{paddocks}"."{WATERED_AREA}") as "{WATERED_AREA}",
	(sum("{paddocks}"."{ESTIMATED_CAPACITY}") / nullif({paddocks}."{AREA}", 0.0)) as "{ESTIMATED_CAPACITY_PER_AREA}",
	(sum("{paddocks}"."{POTENTIAL_CAPACITY}") / nullif({paddocks}."{AREA}", 0.0)) as "{POTENTIAL_CAPACITY_PER_AREA}",
	sum("{paddocks}"."{ESTIMATED_CAPACITY}") as "{ESTIMATED_CAPACITY}",
	sum("{paddocks}"."{POTENTIAL_CAPACITY}") as "{POTENTIAL_CAPACITY}"
from "{paddocks}"
group by "{paddocks}".{TIMEFRAME}
"""
        return super().prepareQuery(query, dependentLayers)

    def __init__(self,
                 dependentLayers,
                 changeset):

        super().__init__(DerivedPropertyLayer.defaultName(),
                         DerivedPropertyLayer.defaultStyle(),
                         dependentLayers,
                         changeset)
