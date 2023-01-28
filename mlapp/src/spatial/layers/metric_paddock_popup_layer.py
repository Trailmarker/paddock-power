# -*- coding: utf-8 -*-
from ..features.paddock_land_type import PaddockLandType
from ..fields.schemas import LAND_TYPE_NAME, PADDOCK, TIMEFRAME
from .derived_feature_layer import DerivedFeatureLayer
from .paddock_land_types_layer import PaddockLandTypesLayer

class MetricPaddockPopupLayer(DerivedFeatureLayer):

    STYLE = "paddock_land_types_popup"

    def prepareQuery(self, query=None):
        [paddockId, timeframe] = [self.metricPaddock.paddockId, self.timeframe]
        
        query = f"""
select *
from "{{0}}"
where "{PADDOCK}" = {paddockId}
and "{TIMEFRAME}" = '{timeframe.name}'
order by "{LAND_TYPE_NAME}"
"""
        return super().prepareQuery(query)

    def __init__(self, metricPaddock, layerName, timeframe):
        
        self.metricPaddock = metricPaddock
        self.timeframe = timeframe

        super().__init__(
            PaddockLandType,
            layerName,
            MetricPaddockPopupLayer.STYLE,
            [PaddockLandTypesLayer])

