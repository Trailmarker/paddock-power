# -*- coding: utf-8 -*-
from qgis.core import QgsFeatureRequest, QgsProject

from ...models.glitch import Glitch
from ..schemas.feature_status import FeatureStatus
from ..features.fence import Fence
from .status_feature_layer import StatusFeatureLayer


class FenceLayer(StatusFeatureLayer):

    STYLE = "fence"

    @classmethod
    def getFeatureType(cls):
        return Fence

    def __init__(self, gpkgFile, layerName, paddockLayer, elevationLayer):
        super().__init__(gpkgFile, layerName, styleName=FenceLayer.STYLE)

        self._paddockLayerId = paddockLayer.id()
        self._elevationLayerId = elevationLayer.id()

    @property
    def paddockLayer(self):
        return QgsProject.instance().mapLayer(self._paddockLayerId)

    @property
    def elevationLayer(self):
        return QgsProject.instance().mapLayer(self._elevationLayerId)

    def wrapFeature(self, feature):
        return self.getFeatureType()(self, self.paddockLayer, self.elevationLayer, feature)

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
            raise Glitch(f"Integrity problem: your Project has multiple Fences with Build Order {buildOrder}")

        return fences[0]
