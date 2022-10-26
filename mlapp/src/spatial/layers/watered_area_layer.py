# -*- coding: utf-8 -*-
from ..features.watered_area import WateredArea
from .derived_layer import DerivedLayer


class WateredAreaLayer(DerivedLayer):

    STYLE = "waterpoint_buffer_new_2"

    QUERY = """
select st_union(geometry), "Waterpoint Buffer Type", "Status"
from "{0}"
group by "Waterpoint Buffer Type", "Status"

"""

    def getFeatureType(cls):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return WateredArea

    def __init__(self, layerName, waterpointBufferLayer):
        super().__init__(layerName, WateredAreaLayer.QUERY, WateredAreaLayer.STYLE, waterpointBufferLayer)
