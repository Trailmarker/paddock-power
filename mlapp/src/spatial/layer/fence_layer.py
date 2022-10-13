# -*- coding: utf-8 -*-
from qgis.core import QgsWkbTypes

from ..feature.fence import Fence, asFence
from .paddock_power_vector_layer import PaddockPowerVectorLayer, PaddockPowerLayerSourceType, PaddockPowerVectorLayerType


class FenceLayer(PaddockPowerVectorLayer):

    STYLE = "fence"

    def __init__(self, sourceType=PaddockPowerLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Fence layer."""

        super(FenceLayer, self).__init__(sourceType,
                                         layerName,
                                         QgsWkbTypes.LineString,
                                         Fence.SCHEMA,
                                         gpkgFile,
                                         styleName=FenceLayer.STYLE)

        # Convert all QGIS features to Fences
        self.setFeatureAdapter(asFence)

    def getLayerType(self):
        """Return the Paddock Power layer type."""
        return PaddockPowerVectorLayerType.Fence

    def updateFence(self, fenceFeature):
        """Update a Fence feature."""
        self.whileEditing(lambda: self.updateFeature(fenceFeature))
