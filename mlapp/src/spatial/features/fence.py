# -*- coding: utf-8 -*-
from qgis.core import QgsFeatureRequest, QgsGeometry, QgsLineString, QgsPoint

from ...models.glitch import Glitch, glitchy
from ...utils import qgsDebug
from ..layers.elevation_layer import ElevationLayer
from ..layers.paddock_layer import PaddockLayer
from .feature import FeatureAction, FeatureStatus, addSchema, actionHandler, editAndRollBack, gatherEdits, persistEdits, upserts
from .line_feature import LineFeature
from .schemas import FenceSchema, BUILD_FENCE


@addSchema(FenceSchema)
class Fence(LineFeature):

    def __init__(self, featureLayer, paddockLayer: PaddockLayer,
                 elevationLayer: ElevationLayer = None, existingFeature=None):
        super().__init__(featureLayer=featureLayer, elevationLayer=elevationLayer, existingFeature=existingFeature)

        assert featureLayer.__class__.__name__ == "FenceLayer", f"featureLayer must be a FenceLayer, not {featureLayer.__class__.__name__}"
        assert isinstance(
            paddockLayer, PaddockLayer), f"paddockLayer must be a PaddockLayer, not {paddockLayer.__class__.__name__}"

        self.paddockLayer = paddockLayer

        self._supersededPaddocks = []
        self._plannedPaddocks = []

    @glitchy()
    def getCrossedPaddocks(self):
        """Get a tuple representing the restriction of this Fence to only Paddocks it completely crosses,
           and the Paddocks that are completely crossed by the specified line."""

        qgsDebug(f"Fence.getCrossedPaddocks: {self.id}")

        fenceLine = self.geometry

        # We are only interested in Paddocks that are current
        existingAndPlannedPaddocks = self.paddockLayer.getFeaturesByStatus(
            FeatureStatus.Built, FeatureStatus.Planned)

        qgsDebug(f"Fence.getCrossedPaddocks: {len(existingAndPlannedPaddocks)} Built or Planned Paddocks")

        qgsDebug(f"Fence.getCrossedPaddocks: fenceLine.__class__.__name__ = {fenceLine.__class__.__name__}")
        qgsDebug(f"Fence.getCrossedPaddocks: fenceLine = {fenceLine.asWkt()}")

        paddockGeometries = [p.geometry.asWkt() for p in existingAndPlannedPaddocks]

        qgsDebug(f"Fence.getCrossedPaddocks: {str(paddockGeometries)} Paddock Geometries")

        intersects = [p for p in existingAndPlannedPaddocks if fenceLine.intersects(p.geometry)]

        qgsDebug(f"[p.name for p in intersects] = {[p.name for p in intersects]}")

        # Find the existing paddocks crossed by the fence line that will be superseded
        crossedPaddocks = []
        for paddock in intersects:
            polygon = paddock.geometry.asMultiPolygon()
            boundaryLine = QgsGeometry.fromMultiPolylineXY(polygon[0])
            intersection = boundaryLine.intersection(fenceLine)
            if intersection.isMultipart():
                qgsDebug("Found a fully crossed paddock")
                # Deep copy the crossed paddocks
                crossedPaddocks.append(self.paddockLayer.makeFeature(paddock))

        qgsDebug(f"[p.name for p in crossedPaddocks] = {[p.name for p in crossedPaddocks]}")

        # Crop the fence line to these superseded paddocks - no loose ends
        allCrossed = QgsGeometry.unaryUnion(p.geometry for p in crossedPaddocks)
        allCrossedBuffered = allCrossed.buffer(5.0, 10)
        normalisedFenceLine = fenceLine.intersection(allCrossedBuffered)

        if normalisedFenceLine.isEmpty():
            qgsDebug("getCrossedPaddocks: normalisedFenceLine is empty")
            return normalisedFenceLine, []

        # If this leaves the fence line multipart, reduce it to a single part
        if normalisedFenceLine.isMultipart():
            qgsDebug("getCrossedPaddocks: normalisedFenceLine is multipart")
            normalisedFenceLine = normalisedFenceLine.combine()

        if normalisedFenceLine.isMultipart():
            raise Glitch(
                "Fence.analyseFence: fence line is still multipart")

        return normalisedFenceLine, crossedPaddocks

    @glitchy()
    def getSupersededAndPlannedPaddocks(self):
        """Get the Paddocks with the specified Build Order."""

        if self.status == FeatureStatus.Drafted:
            return self.getCrossedPaddocks(), []

        buildOrder = self.buildOrder

        if buildOrder <= 0:
            raise Glitch(
                "Fence.getSupersededAndPlannedPaddocks: buildOrder must be a positive integer")

        buildFenceRequest = QgsFeatureRequest().setFilterExpression(f'"{BUILD_FENCE}" = {buildOrder}')

        paddocks = list(self.paddockLayer.getFeatures(request=buildFenceRequest))

        return ([f for f in paddocks if f.status in [FeatureStatus.PlannedSuperseded, FeatureStatus.BuiltSuperseded]],
                [f for f in paddocks if f.status == FeatureStatus.Planned])

    @persistEdits
    @actionHandler(FeatureAction.draft)
    def draftFence(self):
        """Draft a Fence."""

        currentBuildOrder, _, _ = self.featureLayer.getBuildOrder()

        normalisedFenceLine, supersededPaddocks = self.getCrossedPaddocks()

        if normalisedFenceLine is None or normalisedFenceLine.isEmpty() or not supersededPaddocks:
            raise Glitch("The specified Fence does not cross or touch any Paddocks.")

        self.geometry = normalisedFenceLine
        self.buildOrder = currentBuildOrder + 1

        return upserts(self)

    @persistEdits
    @actionHandler(FeatureAction.plan)
    def planFence(self):
        """Plan the Paddocks that would be altered after building this Fence."""

        edits = gatherEdits()

        with editAndRollBack(self.paddockLayer):

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

            self.paddockLayer.splitFeatures(splitLine, False, False)

            existingAndPlannedPaddocks = self.paddockLayer.getFeaturesByStatus(
                FeatureStatus.Built, FeatureStatus.Planned)

            for crossedPaddock in supersededPaddocks:
                crossedPaddockName = crossedPaddock.name

                # Derive the split paddocks
                splitPaddocks = [f for f in existingAndPlannedPaddocks
                                 if f.name == crossedPaddockName]

                for i, splitPaddock in enumerate(splitPaddocks):
                    # If this is one of the 'crossed' paddocks after the split, add, don't update
                    creatingNewPaddock = splitPaddock.id == crossedPaddock.id

                    if creatingNewPaddock:
                        # Try to create an entirely new Paddock feature
                        # Conflicts get quite weird here
                        splitPaddock = self.paddockLayer.copyFeature(splitPaddock)

                    defaultName = crossedPaddockName + ' ' + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]

                    splitPaddock.name = defaultName
                    edits = gatherEdits(edits, splitPaddock.planPaddock(self))

            for paddock in supersededPaddocks:
                edits = gatherEdits(edits, paddock.supersedePaddock(self))

        # self.paddockLayer now rolls back
        return upserts(self, edits)

    @persistEdits
    @actionHandler(FeatureAction.undoPlan)
    def undoPlanFence(self):
        """Undo the plan of Paddocks implied by a Fence."""
        edits = gatherEdits()

        supersededPaddocks, plannedPaddocks = self.getSupersededAndPlannedPaddocks()

        for paddock in supersededPaddocks:
            edits = gatherEdits(edits, paddock.undoSupersedePaddock())

        for paddock in plannedPaddocks:
            edits = gatherEdits(edits, paddock.undoPlanPaddock())

        return upserts(self, edits)
