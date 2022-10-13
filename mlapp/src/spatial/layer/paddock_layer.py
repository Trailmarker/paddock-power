# -*- coding: utf-8 -*-
from qgis.core import QgsFeature, QgsGeometry, QgsWkbTypes

from ...models.paddock_power_error import PaddockPowerError
from ..feature.feature_status import FeatureStatus
from ..feature.fence import Fence
from ..feature.paddock import Paddock, asPaddock
from .paddock_power_vector_layer import PaddockPowerLayerSourceType, PaddockPowerVectorLayer


class PaddockLayer(PaddockPowerVectorLayer):

    STYLE = "paddock"

    def __init__(self, sourceType=PaddockPowerLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Paddock layer."""

        super(PaddockLayer, self).__init__(sourceType,
                                           layerName,
                                           QgsWkbTypes.MultiPolygon,
                                           Paddock.SCHEMA,
                                           gpkgFile,
                                           styleName=self.STYLE)
        # Convert all QGIS features to Paddocks
        self.setFeatureAdapter(asPaddock)

    def getCrossedPaddocks(self, fenceLine):
        """Get a tuple representing the restriction of a line to only Paddocks it completely crosses,
           and the Paddocks that are completely crossed by the specified line."""

        # We are only interested in Paddocks that are current
        existingAndPlannedPaddocks = self.getFeaturesByStatus(
            FeatureStatus.Existing, FeatureStatus.Planned)
        
        intersects = [
            p for p in existingAndPlannedPaddocks if fenceLine.intersects(p.geometry())]

        # Find the existing paddocks crossed by the fence line that will be superseded
        crossedPaddocks = []
        for paddock in intersects:
            polygon = paddock.geometry().asMultiPolygon()
            boundaryLine = QgsGeometry.fromMultiPolylineXY(polygon[0])
            intersection = boundaryLine.intersection(fenceLine)
            if intersection.isMultipart():
                # Deep copy the crossed paddocks
                crossedPaddocks.append(asPaddock(QgsFeature(paddock)))

        # Crop the fence line to these superseded paddocks - no loose ends
        allExisting = QgsGeometry.unaryUnion(
            f.geometry() for f in crossedPaddocks)
        normalisedFenceLine = fenceLine.intersection(allExisting)

        if normalisedFenceLine.isEmpty():
            return fenceLine, [], []

        # If this leaves the fence line multipart, reduce it to a single part
        if normalisedFenceLine.isMultipart():
            normalisedFenceLine = normalisedFenceLine.combine()

        if normalisedFenceLine.isMultipart():
            raise PaddockPowerError(
                "Fence.analyseFence: fence line is still multipart")

        return normalisedFenceLine, crossedPaddocks

    def planPaddocks(self, fence):
        """Get the Paddocks that are Superseded and Planned after splitting this Paddock layer with the specified line."""

        if not isinstance(fence, Fence):
            raise PaddockPowerError(
                "PaddockLayer.planPaddocks: fence must be a Fence")
        
        if fence.status() != FeatureStatus.Draft:
            raise PaddockPowerError(
                "PaddockLayer.planPaddocks: only a Fence with Draft status can be Planned")

        if fence.fenceBuildOrder() <= 0:
            raise PaddockPowerError(
                "PaddockLayer.planPaddocks: fence must have a positive Build Order to be Planned")

        fenceLine = fence.geometry()

        normalisedFenceLine, supersededPaddocks = self.getCrossedPaddocks(fenceLine)

        self.splitFeatures(normalisedFenceLine, False, False)

        existingAndPlannedPaddocks = self.getFeaturesByStatus(FeatureStatus.Existing, FeatureStatus.Planned)

        plannedPaddocks = []
        for crossedPaddock in supersededPaddocks:
            crossedPaddockName = crossedPaddock.featureName()

            # Deep copy the split paddocks
            splitPaddocks = [asPaddock(f) for f in existingAndPlannedPaddocks if f.featureName() == crossedPaddockName and f.id() != crossedPaddock.id()]
            
            for i, splitPaddock in enumerate(splitPaddocks):
                splitPaddock.setFeatureName(
                    crossedPaddockName + ' ' + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i])
                splitPaddock.setStatus(FeatureStatus.Planned)
                splitPaddock.setPaddockBuildFence(fence.fenceBuildOrder())
                splitPaddock.recalculate()
                self.updateFeature(splitPaddock)
                plannedPaddocks.append(splitPaddock)

        for paddock in supersededPaddocks:
            paddock.setStatus(FeatureStatus.Superseded)
            self.updateFeature(paddock)
        
        return normalisedFenceLine, supersededPaddocks, plannedPaddocks

    def undoPlanPaddocks(self, fence):
        """Undo the plan of Paddocks implied by a Fence."""

        if not isinstance(fence, Fence):
            raise PaddockPowerError(
                "PaddockLayer.undoPlanPaddocks: fence must be a Fence")
        
        if fence.status() != FeatureStatus.Planned:
            raise PaddockPowerError(
                "PaddockLayer.undoPlanPaddocks: only a Fence with Planned status can ever be undone")

        buildOrder = fence.fenceBuildOrder()

        if buildOrder <= 0:
            raise PaddockPowerError(
                "PaddockLayer.undoPlanPaddocks: fence must have a positive Build Order to be Planned")

        restoredPaddocks = [asPaddock(f) for f in self.getFeaturesByStatus(FeatureStatus.Superseded) if f.buildFence() == buildOrder]
        undoPlannedPaddocks = [asPaddock(f) for f in self.getFeaturesByStatus(FeatureStatus.Planned) if f.buildFence() == buildOrder]

        for paddock in restoredPaddocks:
            paddock.setStatus(FeatureStatus.Existing)
            self.updateFeature(paddock)

        for paddock in undoPlannedPaddocks:
            self.deleteFeature(paddock)
