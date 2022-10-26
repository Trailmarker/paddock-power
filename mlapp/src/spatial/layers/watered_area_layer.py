# -*- coding: utf-8 -*-
from .derived_layer import DerivedLayer


class WateredAreaLayer(DerivedLayer):

    STYLE = "waterpoint_buffer_new_2"

    QUERY = """
        select st_union(geometry), "Waterpoint Buffer Type", "Status"
        from "{layer}"
        group by "Waterpoint Buffer Type", "Status"
    """

    def __init__(self, layerName, waterpointBufferLayer):
        super().__init__(layerName, waterpointBufferLayer, WateredAreaLayer.QUERY, styleName=WateredAreaLayer.STYLE)
