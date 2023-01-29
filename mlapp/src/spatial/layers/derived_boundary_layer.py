# -*- coding: utf-8 -*-
from ..features.boundary import Boundary
from ..fields.schemas import FID, STATUS, TIMEFRAME, BoundarySchema
from ..fields.timeframe import Timeframe
from .derived_feature_layer import DerivedFeatureLayer
from .paddock_layer import PaddockLayer


class DerivedBoundaryLayer(DerivedFeatureLayer):

    NAME = "Boundary"
    STYLE = "boundary"

    def prepareQuery(self, query, *dependentLayers):
        [paddockLayer] = self.names(*dependentLayers)
        
        query = f"""
select st_union(geometry) as geometry, '{Timeframe.Current.name}' as {TIMEFRAME}, 0 as {FID}
from "{paddockLayer}" where {Timeframe.Current.includesStatuses(f'"{paddockLayer}".{STATUS}')}
union
select st_union(geometry) as geometry, '{Timeframe.Future.name}' as {TIMEFRAME}, 0 as {FID}
from "{paddockLayer}" where {Timeframe.Future.includesStatuses(f'"{paddockLayer}".{STATUS}')}
"""
        return super().prepareQuery(query, *dependentLayers)
    
    def __init__(self,
                 paddockLayer: PaddockLayer):
        
        super().__init__(Boundary, 
                         DerivedBoundaryLayer.NAME, 
                         DerivedBoundaryLayer.STYLE,
                         paddockLayer)


    def getSchema(self):
        """Return the Schema for this layer."""
        return BoundarySchema
        
    
    def getWkbType(self):
        """Return the WKB type for this layer."""
        return BoundarySchema.wkbType
