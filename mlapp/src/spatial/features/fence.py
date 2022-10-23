# -*- coding: utf-8 -*-
from inspect import ismemberdescriptor, ismodule
from qgis.core import QgsFeatureRequest, QgsGeometry, QgsLineString, QgsPoint, QgsPointXY, QgsRectangle

from ...models.glitch import Glitch
from ...utils import qgsDebug
from ..layers.feature_layer import QGSWKB_TYPES
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

    def getFarm(self, glitchBuffer=1.0):
        """Get the farm geometry for this Fence."""
        # Get the whole area around the farm
        # We are only interested in Paddocks that are current
        builtAndPlannedPaddocks = self.paddockLayer.getFeaturesByStatus(
            FeatureStatus.Built, FeatureStatus.Planned)

        # Get the whole current Paddock area - note the buffering here to reduce glitches
        return QgsGeometry.unaryUnion(p.geometry.buffer(glitchBuffer, 10) for p in builtAndPlannedPaddocks)
        # return farm.buffer(-glitchBuffer, 10)

    def getFarmRegion(self):
        """Get the farm geometry for this Fence."""
        # Get the whole area around the farm
        farmExtent = QgsRectangle(self.paddockLayer.extent())
        farmExtent.scale(1.5)  # Expand by 50%
        return QgsGeometry.fromRect(farmExtent)

    def getNotFarm(self, glitchBuffer=1.0):
        """Get the not farm geometry for this Fence."""
        # Get the whole area around the farm
        farmRegion = self.getFarmRegion()
        farm = self.getFarm(glitchBuffer=glitchBuffer)

        # Get a representation of everything that's not in the farm
        notFarm = farmRegion.difference(farm)
        return notFarm.buffer(2 * glitchBuffer, 10)

    def getNewPaddockByLinePart(self, fenceLinePart, notFarm):
        """Get the new paddocks created by this Fence, by line part."""

    @Glitch.glitchy()
    def getNewPaddocks(self, geometry=None):
        """Get the paddocks that are newly enclosed by this Fence, and the normalised outer fence lines."""

        fenceLine = geometry or self.geometry

        if not fenceLine or fenceLine.isEmpty():
            return [], []

        notFarm = self.getNotFarm(glitchBuffer=1.0)

        if notFarm.isEmpty():
            raise Glitch("Cannot find the farm boundary")

        if fenceLine.isEmpty():
            return [], []

        # QgsGeometry.fromPolygonXY([g]) to get the rings as polygons
        _, *farmBoundaries = [QgsGeometry.fromMultiPolylineXY([g]) for g in notFarm.asPolygon()]

        # Straightforward case where we have a single new fence line enclosing things
        if fenceLine.isMultipart():
            fenceLine = fenceLine.asGeometryCollection()[0]

        newPaddocks = []

        for farmBoundary in farmBoundaries:

            intersection = farmBoundary.intersection(fenceLine)

            if (not intersection.isEmpty()) and intersection.isMultipart():
                # We crossed the not-farm boundary more than once, so we are enclosing land
                polyline = fenceLine.asPolyline()
                splitLine = [QgsPointXY(p.x(), p.y()) for p in polyline]

                qgsDebug("getNewPaddocks: splitGeometry in progress …")
                _, splits, _ = notFarm.splitGeometry(splitLine, False)

                # The first result is always the piece of notFarm that is carved out? TODO check this
                if splits:
                    paddockGeometry = notFarm.difference(splits[0])
                    newPaddock = self.paddockLayer.makeFeature()
                    newPaddock.draftPaddock(paddockGeometry, f"Fence {self.buildOrder} New")
                    newPaddocks.append(newPaddock)

        # notFarm = self.getNotFarm(glitchBuffer=1.0)
        # fenceLine = fenceLine.intersection(notFarm)

        if not newPaddocks or not fenceLine:
            return [], []
        else:
            return [fenceLine], newPaddocks

    @Glitch.glitchy()
    def getCrossedPaddocks(self, geometry=None):
        """Get a tuple representing the restriction of this Fence to only Paddocks it completely crosses,
           and the Paddocks that are completely crossed by the specified line."""

        fenceLine = geometry or self.geometry

        if not fenceLine or fenceLine.isEmpty():
            return [], []

        # We are only interested in Paddocks that are current
        builtAndPlannedPaddocks = self.paddockLayer.getFeaturesByStatus(
            FeatureStatus.Built, FeatureStatus.Planned)

        intersects = [p for p in builtAndPlannedPaddocks if fenceLine.intersects(p.geometry)]

        # Crop the fence line to the farm
        farm = self.getFarm(glitchBuffer=1.0)

        # If this makes the fence multipart, we can ignore it
        fenceLine = fenceLine.intersection(farm)

        if fenceLine.isEmpty():
            return [], []

        if fenceLine.isMultipart():
            fenceLine = fenceLine.asGeometryCollection()[0]

        # Find the Built paddocks crossed by the fence line that will be superseded
        crossedPaddocks = []
        for paddock in intersects:
            polygon = paddock.geometry.asMultiPolygon()
            boundaryLine = QgsGeometry.fromMultiPolylineXY(polygon[0])
            intersection = boundaryLine.intersection(fenceLine)
            if intersection.isMultipart():
                crossedPaddocks.append(paddock)

        allCrossed = QgsGeometry.unaryUnion(p.geometry for p in crossedPaddocks)
        allCrossedBuffered = allCrossed.buffer(1.0, 10)
        fenceLine = fenceLine.intersection(allCrossedBuffered)

        if not crossedPaddocks:
            return [], []
        else:
            return [fenceLine], crossedPaddocks

    @Glitch.glitchy()
    def getSupersededAndPlannedPaddocks(self):
        """Get the Paddocks with the specified Build Order."""

        if self.status == FeatureStatus.Drafted:
            _, crossedPaddocks = self.getCrossedPaddocks()
            return crossedPaddocks, []

        buildOrder = self.buildOrder

        if buildOrder <= 0:
            raise Glitch(
                "Fence.getSupersededAndPlannedPaddocks: buildOrder must be a positive integer")

        buildFenceRequest = QgsFeatureRequest().setFilterExpression(f'"{BUILD_FENCE}" = {buildOrder}')

        paddocks = list(self.paddockLayer.getFeatures(request=buildFenceRequest))

        return ([f for f in paddocks if f.status.match(FeatureStatus.PlannedSuperseded, FeatureStatus.BuiltSuperseded)],
                [f for f in paddocks if f.status == FeatureStatus.Planned])

    @Edits.persistEdits
    @FeatureAction.draft.handler()
    def draftFence(self, geometry):
        """Draft a Fence."""

        self.geometry = geometry

        edits = Edits()

        # New Paddocks
        enclosingLines, newPaddocks = self.getNewPaddocks()

        qgsDebug(
            f"draftFence: getNewPaddocks {len(enclosingLines)}, {len(newPaddocks)}, {[p.name for p in newPaddocks]}")

        # Split Paddocks
        splitLines, supersededPaddocks = self.getCrossedPaddocks()

        qgsDebug(
            f"draftFence: getCrossedPaddocks {len(splitLines)}, {len(supersededPaddocks)}, {[p.name for p in supersededPaddocks]}")

        fenceLines = enclosingLines + splitLines

        if (not newPaddocks and not supersededPaddocks) or not fenceLines:
            qgsDebug("draftFence: no new or superseded Paddocks, returning")
            return Edits.delete(self)
            # raise Glitch("The specified Fence does not cross or touch any Built or
            # Planned Paddocks, or enclose any new Paddocks.")

        self.geometry, *fenceLines = fenceLines

        for fenceLine in fenceLines:
            extraFence = self.featureLayer.makeFeature()
            edits = edits.editAfter(extraFence.draftFence(fenceLine))

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

        _, newPaddocks = self.getNewPaddocks()

        qgsDebug(f"planFence: getNewPaddocks {len(newPaddocks)}, {[p.name for p in newPaddocks]}")

        for paddock in newPaddocks:
            edits.editBefore(paddock.planPaddock(self))

        _, supersededPaddocks = self.getCrossedPaddocks()

        qgsDebug(f"planFence: getCrossedPaddocks {len(supersededPaddocks)}, {[p.name for p in supersededPaddocks]}")

        for paddock in supersededPaddocks:
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
