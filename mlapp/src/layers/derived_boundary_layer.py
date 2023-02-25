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

    def prepareQuery(self, query, dependentLayers):
        [basePaddockLayer] = self.names(dependentLayers)

        query = f"""
select st_union(geometry) as geometry,
0 as {FID},
'{Timeframe.Current.name}' as {TIMEFRAME}
from "{basePaddockLayer}"
where {Timeframe.Current.includesStatuses(f'"{basePaddockLayer}".{STATUS}')}
union
select st_union(geometry) as geometry,
0 as {FID},
'{Timeframe.Future.name}' as {TIMEFRAME}
from "{basePaddockLayer}"
where {Timeframe.Future.includesStatuses(f'"{basePaddockLayer}".{STATUS}')}
"""
        return super().prepareQuery(query, dependentLayers)

    def __init__(self,
                 dependentLayers,
                 edits):

        super().__init__(DerivedBoundaryLayer.defaultName(),
                         DerivedBoundaryLayer.defaultStyle(),
                         dependentLayers,
                         None) # Don't try to get fancy
