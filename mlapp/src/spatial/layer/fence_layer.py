# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QMetaType

from qgis.core import QgsFeatureRequest, QgsWkbTypes

from ...utils import guiError
from ..feature.feature_status import FeatureStatus
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

    def fenceCount(self):
        """Get the number of Fences in the layer."""
        return len([f for f in self.getFeatures()])

    def getBuildOrder(self):
        """The lowest Build Order of any Fence in Draft status."""
        fences = list(self.getFeatures())
        if not fences:
            return (0, 0, 0)

        pairs = [(f.fenceBuildOrder(), f) for f in fences]
        pairs.sort(key=lambda p: p[0])

        currentBuildOrder = max([bo for (bo, _) in pairs], default=0)       
        lowestDraftBuildOrder = min([bo for (bo, f) in pairs if f.status() == FeatureStatus.Draft], default=currentBuildOrder+1)
        highestPlannedBuildOrder = max([bo for (bo, f) in pairs if f.status() == FeatureStatus.Planned], default=0)

        return (currentBuildOrder, lowestDraftBuildOrder, highestPlannedBuildOrder)

    def getFenceByBuildOrder(self, buildOrder):
        """Get a Fence by its Build Order."""
        buildOrderRequest = QgsFeatureRequest().setFilterExpression(
            f'"{Fence.BUILD_ORDER}" = {buildOrder}')

        fences = list(self.getFeatures(buildOrderRequest))

        if not fences:
            return None

        if len(fences) > 1:
            guiError(
                f"Integrity problem: your Project has multiple Fences with Build Order {buildOrder}")

        return fences[0]

    def updateFence(self, fenceFeature):
        """Update a Fence feature."""
        self.whileEditing(lambda: self.updateFeature(fenceFeature))
