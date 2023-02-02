# -*- coding: utf-8 -*-
from .features import WaterpointBuffer
from .fields import GRAZING_RADIUS_TYPE, WATERPOINT
from .popup_feature_layer import PopupFeatureLayer


class WaterpointPopupLayer(PopupFeatureLayer):

    STYLE = "waterpoint_popup"

    @classmethod
    def getFeatureType(self):
        return WaterpointBuffer

    def prepareQuery(self, query, *dependentLayers):
        [waterpointBufferLayer] = self.names(*dependentLayers)
        waterpointId = self.waterpoint.FID

        query = f"""
select *
from "{waterpointBufferLayer}"
where "{WATERPOINT}" = {waterpointId}
order by "{GRAZING_RADIUS_TYPE}"
"""
        return super().prepareQuery(query, *dependentLayers)

    def __init__(self,
                 waterpoint):
        
        self.waterpoint = waterpoint

        super().__init__(waterpoint,
                         f"{waterpoint.WATERPOINT_TYPE.value} {waterpoint.FID} Watered Area",
                         WaterpointPopupLayer.defaultStyle(),
                         self.waterpoint.waterpointBufferLayer)
