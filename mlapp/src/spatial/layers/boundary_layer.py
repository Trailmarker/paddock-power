# -*- coding: utf-8 -*-
from ..features.boundary import Boundary
from ..fields.schemas import STATUS, TIMEFRAME
from ..fields.timeframe import Timeframe
from .derived_feature_layer import DerivedFeatureLayer


class BoundaryLayer(DerivedFeatureLayer):

    STYLE = "boundary"

    def parameteriseQuery(self, PaddockLayer):
        return f"""
select st_union(geometry) as geometry, '{Timeframe.Current.name}' as {TIMEFRAME}
from "{PaddockLayer}" where {Timeframe.Current.includesStatuses(f'"{PaddockLayer}".{STATUS}')}
union
select st_union(geometry) as geometry, '{Timeframe.Future.name}' as {TIMEFRAME}
from "{PaddockLayer}" where {Timeframe.Future.includesStatuses(f'"{PaddockLayer}".{STATUS}')}
"""

    def getFeatureType(self):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return Boundary

    def __init__(self, project, layerName, paddockLayer):
        super().__init__(project, layerName, self.parameteriseQuery(paddockLayer.name()), BoundaryLayer.STYLE, paddockLayer)
