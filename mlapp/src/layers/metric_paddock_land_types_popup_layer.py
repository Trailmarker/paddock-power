# -*- coding: utf-8 -*-
from .features import PaddockLandType
from .fields import LAND_TYPE_NAME, PADDOCK, TIMEFRAME, Timeframe
from .popup_feature_layer import PopupFeatureLayer


class MetricPaddockLandTypesPopupLayer(PopupFeatureLayer):

    STYLE = "metric_paddock_land_types_popup"

    @classmethod
    def getFeatureType(cls):
        return PaddockLandType

    def prepareQuery(self, query, *dependentLayers):
        [paddockLandTypesLayer] = self.names(*dependentLayers)
        [paddockId, timeframe] = [self.metricPaddock.PADDOCK, self.layerTimeframe]

        query = f"""
select *
from "{paddockLandTypesLayer}"
where "{PADDOCK}" = {paddockId}
and "{TIMEFRAME}" = '{timeframe.name}'
order by "{LAND_TYPE_NAME}"
"""
        return super().prepareQuery(query, *dependentLayers)

    def __init__(self,
                 metricPaddock,
                 timeframe):

        self.metricPaddock = metricPaddock
        self.layerTimeframe = timeframe

        super().__init__(
            metricPaddock,
            f"{metricPaddock.NAME} {timeframe.name} Land Types",
            MetricPaddockLandTypesPopupLayer.STYLE,
            self.metricPaddock.paddockLandTypesLayer)


class MetricPaddockCurrentLandTypesPopupLayer(MetricPaddockLandTypesPopupLayer):
    """The current land types for a Metric Paddock."""

    def __init__(self, metricPaddock):
        MetricPaddockLandTypesPopupLayer.__init__(self, metricPaddock, Timeframe.Current)


class MetricPaddockFutureLandTypesPopupLayer(MetricPaddockLandTypesPopupLayer):
    """The future land types for a Metric Paddock."""

    def __init__(self, metricPaddock):
        MetricPaddockLandTypesPopupLayer.__init__(self, metricPaddock, Timeframe.Future)
