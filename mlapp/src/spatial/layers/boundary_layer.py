# -*- coding: utf-8 -*-
from .derived_layer import DerivedLayer


class BoundaryLayer(DerivedLayer):

    STYLE = "boundary"

    QUERY = """
        select st_union(geometry) as geometry, 'Built' as "Status"
        from "{layer}" where "Status" in ('Built', 'BuiltSuperseded')
        union
        select st_union(geometry) as geometry, 'Planned' as "Status"
        from "{layer}" where "Status" in ('Built', 'Planned')
    """

    def __init__(self, layerName, paddockLayer):
        super().__init__(layerName, paddockLayer, BoundaryLayer.QUERY, styleName=BoundaryLayer.STYLE)
