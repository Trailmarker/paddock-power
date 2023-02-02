# -*- coding: utf-8 -*-
from qgis.core import QgsFeatureRequest

from ..models import Glitch
from .features import Fence
from .fields import BUILD_ORDER, FeatureStatus
from .persisted_feature_layer import PersistedFeatureLayer


class FenceLayer(PersistedFeatureLayer):

    LAYER_NAME = "Fences"
    STYLE = "fence"

    @classmethod
    def getFeatureType(cls):
        return Fence

    def __init__(self,
                 workspaceFile):
        super().__init__(workspaceFile,
                         layerName=FenceLayer.defaultName(),
                         styleName=FenceLayer.defaultStyle())

    def getBuildOrder(self):
        """The lowest Build Order of any Fence in Draft status."""
        fences = list(self.getFeatures())
        if not fences:
            return (0, 0, 0)

        pairs = [(f.BUILD_ORDER, f) for f in fences]
        pairs.sort(key=lambda p: p[0])

        currentBuildOrder = max([bo for (bo, _) in pairs], default=0)
        lowestDraftBuildOrder = min(
            [bo for(bo, f) in pairs if f.STATUS == FeatureStatus.Drafted],
            default=currentBuildOrder + 1)
        highestPlannedBuildOrder = max([bo for (bo, f) in pairs if f.STATUS == FeatureStatus.Planned], default=0)

        return (currentBuildOrder, lowestDraftBuildOrder, highestPlannedBuildOrder)

    def getFenceByBuildOrder(self, buildOrder):
        """Get a Fence by its Build Order."""
        buildOrderRequest = QgsFeatureRequest().setFilterExpression(
            f'"{BUILD_ORDER}" = {buildOrder}')

        fences = list(self.getFeatures(buildOrderRequest))

        if not fences:
            return None

        if len(fences) > 1:
            raise Glitch(f"Integrity problem: your Workspace has multiple Fences with Build Order {buildOrder}")

        return fences[0]
