# -*- coding: utf-8 -*-
from ..features.waterpoint_buffer import WaterpointBuffer
from ..fields.schemas import GRAZING_RADIUS_TYPE, WATERPOINT, WaterpointBufferSchema
from .derived_feature_layer import DerivedFeatureLayer


class WaterpointPopupLayer(DerivedFeatureLayer):

    STYLE = "waterpoint_popup"

    def prepareQuery(self, query, *dependentLayers):
        waterpointId = self.waterpoint.FID

        query = f"""
select *
from "{{0}}"
where "{WATERPOINT}" = {waterpointId}
order by "{GRAZING_RADIUS_TYPE}"
"""
        return super().prepareQuery(query)

    def __init__(self, waterpoint, layerName):
        # Burn in the Waterpoint specific parameters first …
        self.waterpoint = waterpoint
        super().__init__(WaterpointBuffer, layerName, WaterpointPopupLayer.STYLE, ["WaterpointBufferLayer"])

    def getSchema(self):
        """Return the Schema for this layer."""
        return WaterpointBufferSchema

    def getWkbType(self):
        """Return the WKB type for this layer."""
        return WaterpointBufferSchema.wkbType
