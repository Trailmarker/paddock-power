# -*- coding: utf-8 -*-
from qgis.core import QgsFeature, QgsFeatureRequest, QgsGeometry, QgsLineString, QgsPoint, QgsWkbTypes

from ...models.paddock_power_error import PaddockPowerError
from ...utils import qgsDebug
from ..feature.feature_status import FeatureStatus
from ..feature.fence import Fence
from ..feature.paddock import Paddock, asPaddock, makePaddock
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
        existingAndPlannedPaddocks = self.getFeaturesByStatus(FeatureStatus.Existing, FeatureStatus.Planned)

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
        allCrossed = QgsGeometry.unaryUnion(
            f.geometry() for f in crossedPaddocks)
        allCrossedBuffered = allCrossed.buffer(5.0, 10)
        normalisedFenceLine = fenceLine.intersection(allCrossedBuffered)

        if normalisedFenceLine.isEmpty():
            return normalisedFenceLine, []

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

        maximumFid = self.maximumValue(
            self.fields().indexFromName(Paddock.FID))
        maximumFid = maximumFid + 100

        fenceLine = fence.geometry()

        _, supersededPaddocks = self.getCrossedPaddocks(
            fenceLine)

        polyline = fenceLine.asPolyline()
        points = [QgsPoint(p.x(), p.y()) for p in polyline]
        splitLine = QgsLineString(points)

        self.splitFeatures(splitLine, False, False)

        existingAndPlannedPaddocks = self.getFeaturesByStatus(
            FeatureStatus.Existing, FeatureStatus.Planned)

        plannedPaddocks = []

        for crossedPaddock in supersededPaddocks:
            crossedPaddockName = crossedPaddock.featureName()

            # Derive the split paddocks
            splitPaddocks = [asPaddock(f) for f in existingAndPlannedPaddocks
                             if f.featureName() == crossedPaddockName]

            for i, splitPaddock in enumerate(splitPaddocks):
                # If this is one of the 'crossed' paddocks after the split, add, don't update
                creatingNewPaddock = splitPaddock.id() == crossedPaddock.id()

                if creatingNewPaddock:
                    # Try to create an entirely new Paddock feature
                    # Conflicts get quite weird here
                    newPaddock = QgsFeature(self.fields())

                    for field in self.fields():
                        if field.name() != Paddock.FID:
                            newPaddock.setAttribute(
                                field.name(), splitPaddock.attribute(field.name()))

                    newPaddock.setGeometry(splitPaddock.geometry())
                    splitPaddock = asPaddock(newPaddock)

                defaultName = crossedPaddockName + ' ' + \
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]
                splitPaddock.setFeatureName(defaultName)
                splitPaddock.setStatus(FeatureStatus.Planned)
                splitPaddock.setPaddockBuildFence(fence.fenceBuildOrder())
                splitPaddock.recalculate()

                if creatingNewPaddock:
                    # Add the new Paddock
                    self.addFeature(splitPaddock)
                else:
                    self.updateFeature(splitPaddock)

                plannedPaddocks.append(splitPaddock)

        for paddock in supersededPaddocks:
            paddock.setPaddockBuildFence(fence.fenceBuildOrder())
            paddock.setStatus(FeatureStatus.Superseded)
            self.updateFeature(paddock)

        return supersededPaddocks, plannedPaddocks

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

        buildFenceRequest = QgsFeatureRequest().setFilterExpression(
            f'"{Paddock.BUILD_FENCE}" = {buildOrder}')

        restoredPaddocks = self.getFeaturesByStatus(
            FeatureStatus.Superseded, request=buildFenceRequest)
        undoPlannedPaddocks = self.getFeaturesByStatus(
            FeatureStatus.Planned, request=buildFenceRequest)

        for paddock in restoredPaddocks:
            # Could be a few issues here …
            paddock.setStatus(FeatureStatus.Existing)
            paddock.setPaddockBuildFence(0)
            self.updateFeature(paddock)

        for paddock in undoPlannedPaddocks:
            self.deleteFeature(paddock.id())

    def getPaddocksByBuildOrder(self, buildFence):
        """Get the Paddocks with the specified Build Order."""

        if buildFence <= 0:
            raise PaddockPowerError(
                "PaddockLayer.getPaddocksByBuildOrder: buildOrder must be a positive integer")

        buildFenceRequest = QgsFeatureRequest().setFilterExpression(
            f'"{Paddock.BUILD_FENCE}" = {buildFence}')

        fencePaddocks = list(self.getFeatures(request=buildFenceRequest))

        return ([f for f in fencePaddocks if f.status() == FeatureStatus.Superseded],
                [f for f in fencePaddocks if f.status() == FeatureStatus.Planned])

    def getPaddocksByFence(self, fence):
        """Get the Paddocks with the specified Build Order."""

        if fence.status() == FeatureStatus.Draft:
            _, supersededPaddocks = self.getCrossedPaddocks(
                fence.geometry())
            return supersededPaddocks, []

        buildOrder = fence.fenceBuildOrder()

        if buildOrder <= 0:
            raise PaddockPowerError(
                "PaddockLayer.getPaddocksByBuildOrder: buildOrder must be a positive integer")

        return self.getPaddocksByBuildOrder(buildOrder)

    def updateFencePaddocks(self, fence):
        """Update the superseded and planned Paddocks for a Fence."""
        supersededPaddocks, plannedPaddocks = self.getPaddocksByFence(fence)

        fence.setSupersededPaddocks(supersededPaddocks)
        fence.setPlannedPaddocks(plannedPaddocks)
        
