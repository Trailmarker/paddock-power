# -*- coding: utf-8 -*-
from qgis.core import QgsWkbTypes

from ..feature.waterpoint import Waterpoint, asWaterpoint
from .paddock_power_vector_layer import PaddockPowerVectorLayer, PaddockPowerLayerSourceType


class WaterpointLayer(PaddockPowerVectorLayer):

    STYLE = "waterpoint"

    def __init__(self, sourceType=PaddockPowerLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Waterpoint layer."""

        super(WaterpointLayer, self).__init__(sourceType,
                                              layerName,
                                              QgsWkbTypes.Point,
                                              Waterpoint.SCHEMA,
                                              gpkgFile,
                                              styleName=self.STYLE)

        # Convert all QGIS features to Waterpoint objects
        self.setFeatureAdapter(asWaterpoint)
