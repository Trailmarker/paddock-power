# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QMetaType

from qgis.core import QgsFeatureRequest, QgsWkbTypes

from ...models.paddock_power_error import PaddockPowerError
from ...utils import guiError
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
        if self.featureCount() == 0:
            return 0
        
        fields = self.fields()
        buildOrderIndex = fields.indexFromName(Fence.BUILD_ORDER)
        
        return max(self.maximumValue(buildOrderIndex), 0)

    def nextBuildOrder(self):
        """Get the next Fence Build Order."""
        return self.currentBuildOrder() + 1

    def getFenceByBuildOrder(self, buildOrder):
        """Get a Fence by its Build Order."""
        buildOrderRequest = QgsFeatureRequest().setFilterExpression(f'"{Fence.BUILD_ORDER}" = {buildOrder}')
        
        fences = list(self.getFeatures(buildOrderRequest))

        if not fences:
            return None

        if len(fences) > 1:
            guiError(f"Integrity problem: your Project has multiple Fences with Build Order {buildOrder}")

        return fences[0]

    def updateFence(self, fenceFeature):
        """Update a Fence feature."""
        self.whileEditing(lambda: self.updateFeature(fenceFeature))
