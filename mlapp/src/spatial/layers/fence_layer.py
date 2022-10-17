# -*- coding: utf-8 -*-
from numpy import isin
from qgis.core import QgsFeatureRequest

from ...utils import guiError
from ..features.feature_status import FeatureStatus
from ..features.fence import Fence
from .elevation_layer import ElevationLayer
from .feature_layer import FeatureLayer, FeatureLayerSourceType
from .paddock_layer import PaddockLayer


class FenceLayer(FeatureLayer):

    STYLE = "fence"

    def __init__(self, paddockLayer: PaddockLayer, elevationLayer: ElevationLayer,
                 sourceType=FeatureLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Fence layer."""

        super().__init__(Fence,
                         sourceType,
                         layerName,
                         gpkgFile,
                         styleName=FenceLayer.STYLE)

        assert isinstance(paddockLayer, PaddockLayer)
        assert isinstance(elevationLayer, ElevationLayer)

        self.paddockLayer = paddockLayer

        self.wrapFeature = lambda feature: Fence(featureLayer=self, paddockLayer=self.paddockLayer, elevationLayer=elevationLayer, existingFeature=feature)

    def getBuildOrder(self):
        """The lowest Build Order of any Fence in Draft status."""
        fences = list(self.getFeatures())
        if not fences:
            return (0, 0, 0)

        pairs = [(f.buildOrder, f) for f in fences]
        pairs.sort(key=lambda p: p[0])

        currentBuildOrder = max([bo for (bo, _) in pairs], default=0)
        lowestDraftBuildOrder = min(
            [bo for(bo, f) in pairs if f.status == FeatureStatus.Drafted],
            default=currentBuildOrder + 1)
        highestPlannedBuildOrder = max([bo for (bo, f) in pairs if f.status == FeatureStatus.Planned], default=0)

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
