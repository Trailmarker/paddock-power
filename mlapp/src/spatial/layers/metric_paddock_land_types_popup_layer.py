# -*- coding: utf-8 -*-
from ..features.paddock_land_type import PaddockLandType
from ..fields.schemas import LAND_TYPE_NAME, PADDOCK, TIMEFRAME, PaddockLandTypeSchema
from ..fields.timeframe import Timeframe
from .derived_feature_layer import DerivedFeatureLayer


class MetricPaddockLandTypesPopupLayer(DerivedFeatureLayer):

    STYLE = "metric_paddock_land_types_popup"

    def prepareQuery(self, query, *dependentLayers):
        [paddockLandTypesLayer] = self.names(*dependentLayers)
        [paddockId, timeframe] = [self.metricPaddock.PADDOCK, self.timeframe]

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
        self.timeframe = timeframe

        layerName = f"{metricPaddock.NAME} {timeframe.name} Paddock Land Types"

        super().__init__(
            PaddockLandType,
            layerName,
            MetricPaddockLandTypesPopupLayer.STYLE,
            self.metricPaddock.paddockLandTypesLayer)

    def getSchema(self):
        """Return the Schema for this layer."""
        return PaddockLandTypeSchema

    def getWkbType(self):
        """Return the WKB type for this layer."""
        return PaddockLandTypeSchema.wkbType


class MetricPaddockCurrentLandTypesPopupLayer(MetricPaddockLandTypesPopupLayer):
    """The current land types for a Metric Paddock."""

    def __init__(self, metricPaddock):
        MetricPaddockLandTypesPopupLayer.__init__(self, metricPaddock, Timeframe.Current)


class MetricPaddockFutureLandTypesPopupLayer(MetricPaddockLandTypesPopupLayer):
    """The future land types for a Metric Paddock."""

    def __init__(self, metricPaddock):
        MetricPaddockLandTypesPopupLayer.__init__(self, metricPaddock, Timeframe.Future)
