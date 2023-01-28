# -*- coding: utf-8 -*-
from ..features.boundary import Boundary
from ..fields.schemas import STATUS, TIMEFRAME
from ..fields.timeframe import Timeframe
from .derived_feature_layer import DerivedFeatureLayer
from .paddock_layer import PaddockLayer


class DerivedBoundaryLayer(DerivedFeatureLayer):

    NAME = "Boundary"
    STYLE = "boundary"

    def prepareQuery(self, query=None):
        
        [paddockLayer] = self.names(PaddockLayer)
        
        query = f"""
select st_union(geometry) as geometry, '{Timeframe.Current.name}' as {TIMEFRAME}
from "{paddockLayer}" where {Timeframe.Current.includesStatuses(f'"{paddockLayer}".{STATUS}')}
union
select st_union(geometry) as geometry, '{Timeframe.Future.name}' as {TIMEFRAME}
from "{paddockLayer}" where {Timeframe.Future.includesStatuses(f'"{paddockLayer}".{STATUS}')}
"""
        return super().prepareQuery(query)
    
    def __init__(self):
        super().__init__(Boundary, 
                         DerivedBoundaryLayer.NAME, 
                         DerivedBoundaryLayer.STYLE,
                         [PaddockLayer])
