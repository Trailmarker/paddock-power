# -*- coding: utf-8 -*-
from ..features.waterpoint_buffer import WaterpointBuffer
from ..schemas.schemas import GRAZING_RADIUS_TYPE, WATERPOINT
from .derived_feature_layer import DerivedFeatureLayer


class WaterpointPopupLayer(DerivedFeatureLayer):

    STYLE = "waterpoint_popup"

    def parameteriseQuery(self, waterpointId):
        return f"""
select *
from "{{0}}"
where "{WATERPOINT}" = {waterpointId}
order by "{GRAZING_RADIUS_TYPE}"
"""

    def getFeatureType(cls):
        """Return the type of feature that this layer contains. Override in subclasses"""
        return WaterpointBuffer

    def __init__(self, project, layerName, waterpoint, waterpointBufferLayer):
        # Burn in the Waterpoint specific parameters first …
        query = self.parameteriseQuery(waterpointId=waterpoint.id)

        super().__init__(project, layerName, query, WaterpointPopupLayer.STYLE, waterpointBufferLayer)
