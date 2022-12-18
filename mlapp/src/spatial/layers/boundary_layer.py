# -*- coding: utf-8 -*-
from ..features.boundary import Boundary
from .derived_feature_layer import DerivedFeatureLayer


class BoundaryLayer(DerivedFeatureLayer):

    STYLE = "boundary"

    QUERY = """
select st_union(geometry) as geometry, 'Built' as "Status"
from "{0}" where "Status" in ('Built', 'BuiltSuperseded')
union
select st_union(geometry) as geometry, 'Planned' as "Status"
from "{0}" where "Status" in ('Built', 'Planned')

"""

    def getFeatureType(cls):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return Boundary

    def __init__(self, project, layerName, paddockLayer):
        super().__init__(project, layerName, BoundaryLayer.QUERY, BoundaryLayer.STYLE, paddockLayer)
