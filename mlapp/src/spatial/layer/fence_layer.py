# -*- coding: utf-8 -*-
from qgis.core import QgsFeatureRequest, QgsWkbTypes

from ..feature.fence import Fence, asFence
from .paddock_power_vector_layer import PaddockPowerVectorLayer, PaddockPowerLayerSourceType


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

    def currentBuildOrder(self):
        """Get the last planned Fence Build Order."""
        fields = self.fields()
        buildOrderIndex = fields.indexFromName(Fence.BUILD_ORDER)
        
        currentBuildOrder = self.maximumValue(buildOrderIndex, 1000)
        return max(currentBuildOrder, 0)

    def nextBuildOrder(self):
        """Get the next Fence Build Order."""
        return self.currentBuildOrder() + 1

    def getFenceByBuildOrder(self, buildOrder):
        """Get a Fence by its Build Order."""
        buildOrderRequest = QgsFeatureRequest().setFilterExpression(f'"Build Order" = {buildOrder}')
        
        return self.getFeatures(buildOrderRequest)

    def updateFence(self, fenceFeature):
        """Update a Fence feature."""
        self.whileEditing(lambda: self.updateFeature(fenceFeature))
