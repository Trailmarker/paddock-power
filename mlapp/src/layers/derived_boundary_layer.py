# -*- coding: utf-8 -*-
from .features import Boundary
from .fields import FID, STATUS, TIMEFRAME, Timeframe
from .derived_feature_layer import DerivedFeatureLayer


class DerivedBoundaryLayer(DerivedFeatureLayer):

    LAYER_NAME = "Derived Boundary"
    STYLE = "boundary"

    @classmethod
    def getFeatureType(cls):
        return Boundary

    def prepareQuery(self, query, *dependentLayers):
        [basePaddockLayer] = self.names(*dependentLayers)

        query = f"""
select st_union(geometry) as geometry, '{Timeframe.Current.name}' as {TIMEFRAME}, 0 as {FID}
from "{basePaddockLayer}" where {Timeframe.Current.includesStatuses(f'"{basePaddockLayer}".{STATUS}')}
union
select st_union(geometry) as geometry, '{Timeframe.Future.name}' as {TIMEFRAME}, 0 as {FID}
from "{basePaddockLayer}" where {Timeframe.Future.includesStatuses(f'"{basePaddockLayer}".{STATUS}')}
"""
        return super().prepareQuery(query, *dependentLayers)

    def __init__(self,
                 basePaddockLayer):

        super().__init__(DerivedBoundaryLayer.defaultName(),
                         DerivedBoundaryLayer.defaultStyle(),
                         basePaddockLayer)
