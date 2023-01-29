# -*- coding: utf-8 -*-
from qgis.core import QgsFeatureRequest

from ...models.glitch import Glitch
from ..features.fence import Fence
from ..fields.feature_status import FeatureStatus
from ..fields.names import BUILD_ORDER
from ..fields.schemas import FenceSchema
from .persisted_feature_layer import PersistedFeatureLayer


class FenceLayer(PersistedFeatureLayer):

    NAME = "Fences"
    STYLE = "fence"

    def __init__(self,
                 workspaceFile):
        super().__init__(Fence,
                         workspaceFile,
                         layerName=FenceLayer.NAME,
                         styleName=FenceLayer.STYLE)

    def getSchema(self):
        """Return the Schema for this layer."""
        return FenceSchema

    def getWkbType(self):
        """Return the WKB type for this layer."""
        return FenceSchema.wkbType

    def getBuildOrder(self):
        """The lowest Build Order of any Fence in Draft status."""
        fences = list(self.getFeatures())
        if not fences:
            return (0, 0, 0)

        pairs = [(f.BUILD_ORDER, f) for f in fences]
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
            f'"{BUILD_ORDER}" = {buildOrder}')

        fences = list(self.getFeatures(buildOrderRequest))

        if not fences:
            return None

        if len(fences) > 1:
            raise Glitch(f"Integrity problem: your Workspace has multiple Fences with Build Order {buildOrder}")

        return fences[0]
