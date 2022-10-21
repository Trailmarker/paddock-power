# -*- coding: utf-8 -*-
from qgis.core import QgsFeatureRequest, QgsGeometry, QgsLineString, QgsPoint

from ...models.glitch import Glitch
from ...utils import qgsDebug
from ..layers.elevation_layer import ElevationLayer
from ..layers.paddock_layer import PaddockLayer
from .edits import Edits
from .feature import FeatureAction
from .feature_status import FeatureStatus
from .line_feature import LineFeature
from .schemas import FenceSchema, BUILD_FENCE


@FenceSchema.addSchema()
class Fence(LineFeature):

    def __init__(self, featureLayer, paddockLayer: PaddockLayer,
                 elevationLayer: ElevationLayer = None, existingFeature=None):
        super().__init__(featureLayer=featureLayer, elevationLayer=elevationLayer, existingFeature=existingFeature)

        self.paddockLayer = paddockLayer

        self._supersededPaddocks = []
        self._plannedPaddocks = []

    @property
    def title(self):
        return f"Fence {self.buildOrder}: ({self.featureLength} km)"

    @property
    def isInfrastructure(self):
        """Return True for Fence."""
        return True

    @Glitch.glitchy()
    def getCrossedPaddocks(self):
        """Get a tuple representing the restriction of this Fence to only Paddocks it completely crosses,
           and the Paddocks that are completely crossed by the specified line."""

        # qgsDebug(f"Fence.getCrossedPaddocks: {self.id}")

        fenceLine = self.geometry

        # We are only interested in Paddocks that are current
        builtAndPlannedPaddocks = self.paddockLayer.getFeaturesByStatus(
            FeatureStatus.Built, FeatureStatus.Planned)

        # qgsDebug(f"Fence.getCrossedPaddocks: {len(builtAndPlannedPaddocks)} Built or Planned Paddocks")

        # qgsDebug(f"Fence.getCrossedPaddocks: fenceLine.__class__.__name__ = {fenceLine.__class__.__name__}")
        # qgsDebug(f"Fence.getCrossedPaddocks: fenceLine = {fenceLine.asWkt()}")

        intersects = [p for p in builtAndPlannedPaddocks if fenceLine.intersects(p.geometry)]

        # qgsDebug(f"[p for p in intersects] = {str([p for p in intersects])}")

        # Find the Built paddocks crossed by the fence line that will be superseded
        crossedPaddocks = []
        for paddock in intersects:
            polygon = paddock.geometry.asMultiPolygon()
            boundaryLine = QgsGeometry.fromMultiPolylineXY(polygon[0])
            intersection = boundaryLine.intersection(fenceLine)
            if intersection.isMultipart():
                qgsDebug("Found a fully crossed paddock")
                crossedPaddocks.append(paddock)

        # Crop the fence line to these superseded paddocks - no loose ends
        allCrossed = QgsGeometry.unaryUnion(p.geometry for p in crossedPaddocks)
        allCrossedBuffered = allCrossed.buffer(5.0, 10)
        normalisedFenceLine = fenceLine.intersection(allCrossedBuffered)

        if normalisedFenceLine.isEmpty():
            # qgsDebug("getCrossedPaddocks: normalisedFenceLine is empty")
            return [], []

        if normalisedFenceLine.isMultipart():
            # qgsDebug("getCrossedPaddocks: normalisedFenceLine is multipart")
            return [line for line in normalisedFenceLine.asGeometryCollection()], crossedPaddocks

        # qgsDebug("getCrossedPaddocks: normalisedFenceLine is singlepart")
        return [normalisedFenceLine], crossedPaddocks

        # # This can still happen, for example if a Fence is split across two separate Paddocks
        # if normalisedFenceLine.isMultipart():
        #     qgsDebug("getCrossedPaddocks: normalisedFenceLine is multipart")
        #     # normalisedFenceLine = normalisedFenceLine.combine()
        #     if normalisedFenceLine.isMultipart():
        #         for part in normalisedFenceLine.asGeometryCollection():
        #             qgsDebug(f"getCrossedPaddocks: part = {part.asWkt()}")

        #         raise Glitch(
        #             "Fence.analyseFence: fence line is still multipart")

    @Glitch.glitchy()
    def getSupersededAndPlannedPaddocks(self):
        """Get the Paddocks with the specified Build Order."""

        if self.status == FeatureStatus.Drafted:
            _, crossedPaddocks = self.getCrossedPaddocks()
            return crossedPaddocks, []

        buildOrder = self.buildOrder

        # qgsDebug(f"Fence.getSupersededAndPlannedPaddocks: buildOrder = {buildOrder}")

        if buildOrder <= 0:
            raise Glitch(
                "Fence.getSupersededAndPlannedPaddocks: buildOrder must be a positive integer")

        buildFenceRequest = QgsFeatureRequest().setFilterExpression(f'"{BUILD_FENCE}" = {buildOrder}')

        paddocks = list(self.paddockLayer.getFeatures(request=buildFenceRequest))

        # qgsDebug(f"Fence.getSupersededAndPlannedPaddocks: {str(paddocks)} with Build Fence {buildOrder}")

        return ([f for f in paddocks if f.status.match(FeatureStatus.PlannedSuperseded, FeatureStatus.BuiltSuperseded)],
                [f for f in paddocks if f.status == FeatureStatus.Planned])

    @Edits.persistEdits
    @FeatureAction.draft.handler()
    def draftFence(self):
        """Draft a Fence."""
        edits = Edits()

        normalisedFenceLines, supersededPaddocks = self.getCrossedPaddocks()

        if normalisedFenceLines is None or not supersededPaddocks:
            raise Glitch("The specified Fence does not cross or touch any Built or Planned Paddocks.")

        if len(normalisedFenceLines) > 1:
            normalisedFenceLine, *normalisedFenceLines = normalisedFenceLines

            for fenceLine in normalisedFenceLines:
                extraFence = self.featureLayer.makeFeatureFromGeometry(fenceLine)
                edits = edits.editAfter(extraFence.draftFence())
        else:
            normalisedFenceLine = normalisedFenceLines[0]

        self.geometry = normalisedFenceLine

        currentBuildOrder, _, _ = self.featureLayer.getBuildOrder()
        self.buildOrder = currentBuildOrder + 1

        return Edits.upsert(self).editBefore(edits)

    @Edits.persistEdits
    @FeatureAction.plan.handler()
    def planFence(self):
        """Plan the Paddocks that would be altered after building this Fence."""

        edits = Edits()

        with Edits.editAndRollBack(self.paddockLayer):

            _, lowestDraftBuildOrder, _ = self.featureLayer.getBuildOrder()

            if self.buildOrder > lowestDraftBuildOrder:
                raise Glitch(
                    "You must Plan your Drafted Fences from first to last according to Build Order.")

            if self.buildOrder <= 0:
                raise Glitch("Fence must have a positive Build Order to be Planned")

            _, supersededPaddocks = self.getCrossedPaddocks()

            fenceLine = self.geometry
            polyline = fenceLine.asPolyline()
            points = [QgsPoint(p.x(), p.y()) for p in polyline]
            splitLine = QgsLineString(points)

            builtAndPlannedPaddocks = self.paddockLayer.getFeaturesByStatus(
                FeatureStatus.Built, FeatureStatus.Planned)

            self.paddockLayer.splitFeatures(splitLine, False, False)

            builtAndPlannedPaddocks = self.paddockLayer.getFeaturesByStatus(
                FeatureStatus.Built, FeatureStatus.Planned)

            for crossedPaddock in supersededPaddocks:
                crossedPaddockName = crossedPaddock.name

                # Deep copy all split paddocks
                splitPaddocks = [self.paddockLayer.copyFeature(f)
                                 for f in builtAndPlannedPaddocks
                                 if f.name == crossedPaddockName]

                for i, splitPaddock in enumerate(splitPaddocks):
                    defaultName = crossedPaddockName + ' ' + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]
                    splitPaddock.name = defaultName
                    # Note this is set explicitly to Drafted because
                    # the Paddock is derived in a dodgy way using splitFeatures
                    splitPaddock.status = FeatureStatus.Drafted
                    splitPaddock.recalculate()
                    edits.editBefore(splitPaddock.planPaddock(self))

        _, supersededPaddocks = self.getCrossedPaddocks()

        for paddock in supersededPaddocks:
            paddock.recalculate()
            edits.editBefore(paddock.supersedePaddock(self))

        # self.paddockLayer now rolls back
        return Edits.upsert(self).editAfter(edits)

    @Edits.persistEdits
    @FeatureAction.undoPlan.handler()
    def undoPlanFence(self):
        """Undo the plan of Paddocks implied by a Fence."""
        edits = Edits()

        supersededPaddocks, plannedPaddocks = self.getSupersededAndPlannedPaddocks()

        # qgsDebug(f"supersededPaddocks = {str(supersededPaddocks)}")
        # qgsDebug(f"plannedPaddocks = {str(plannedPaddocks)}")

        for paddock in supersededPaddocks:
            edits = edits.editBefore(paddock.undoSupersedePaddock())

        for paddock in plannedPaddocks:
            edits = edits.editBefore(paddock.undoPlanPaddock())

        return Edits.upsert(self).editAfter(edits)
