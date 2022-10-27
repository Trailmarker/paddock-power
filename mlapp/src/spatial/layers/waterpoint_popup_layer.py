# -*- coding: utf-8 -*-
from ..features.waterpoint_buffer import WaterpointBuffer
from .derived_layer import DerivedLayer


class WaterpointPopupLayer(DerivedLayer):

    STYLE = "waterpoint_buffer_new_2"

    QUERY = """
select * from "{{0}}"
where "Waterpoint" = {waterpointId}
"""

    def getFeatureType(cls):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return WaterpointBuffer

    def __init__(self, layerName, waterpoint, waterpointBufferLayer):
        # Burn in the Waterpoint specific parameters first …
        query = WaterpointPopupLayer.QUERY.format(waterpointId=waterpoint.id)

        super().__init__(layerName, query, WaterpointPopupLayer.STYLE, waterpointBufferLayer)
