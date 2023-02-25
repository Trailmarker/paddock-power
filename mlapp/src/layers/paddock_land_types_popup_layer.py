# -*- coding: utf-8 -*-
from .features import PaddockLandType
from .fields import LAND_TYPE_NAME, PADDOCK, TIMEFRAME, Timeframe
from .popup_feature_layer import PopupFeatureLayer


class PaddockLandTypesPopupLayer(PopupFeatureLayer):

    STYLE = "paddock_land_types_popup"

    @classmethod
    def getFeatureType(cls):
        return PaddockLandType

    def prepareQuery(self, query, *dependentLayers):
        [paddockLandTypesLayer] = self.names(*dependentLayers)
        [paddockId, timeframe] = [self.paddock.PADDOCK, self.layerTimeframe]

        query = f"""
select *
from "{paddockLandTypesLayer}"
where "{PADDOCK}" = {paddockId}
and "{TIMEFRAME}" = '{timeframe.name}'
order by "{LAND_TYPE_NAME}"
"""
        return super().prepareQuery(query, *dependentLayers)

    def __init__(self,
                 paddock,
                 timeframe):

        self.paddock = paddock
        self.layerTimeframe = timeframe

        super().__init__(
            paddock,
            f"{paddock.NAME} {timeframe.name} Land Types",
            PaddockLandTypesPopupLayer.defaultStyle(),
            self.paddock.paddockLandTypesLayer)


class PaddockCurrentLandTypesPopupLayer(PaddockLandTypesPopupLayer):
    """The current land types for a Paddock."""

    def __init__(self, paddock):
        PaddockLandTypesPopupLayer.__init__(self, paddock, Timeframe.Current)


class PaddockFutureLandTypesPopupLayer(PaddockLandTypesPopupLayer):
    """The future land types for a Paddock."""

    def __init__(self, paddock):
        PaddockLandTypesPopupLayer.__init__(self, paddock, Timeframe.Future)
