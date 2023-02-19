# -*- coding: utf-8 -*-
from collections import defaultdict
from qgis.core import QgsFeatureRequest, QgsGeometry, QgsLineString, QgsPoint, QgsPointXY

from ...models import Glitch
from ...utils import PLUGIN_NAME, qgsDebug
from ..fields import BUILD_FENCE, FeatureStatus, Timeframe, FenceSchema
from .edits import Edits
from .feature_action import FeatureAction
from .persisted_feature import PersistedFeature
from .status_feature_mixin import StatusFeatureMixin


@FenceSchema.addSchema()
class Fence(PersistedFeature, StatusFeatureMixin):

    def __init__(self, featureLayer, existingFeature=None):
        PersistedFeature.__init__(self, featureLayer, existingFeature)
        StatusFeatureMixin.__init__(self)

        self._supersededPaddocks = []
        self._plannedPaddocks = []

    @property
    def TITLE(self):
        return f"{self.NAME} ({self.LENGTH} km)"

    @property
    def isInfrastructure(self):
        """Return True for Fence."""
        return True

    @property
    def basePaddockLayer(self):
        return self.featureLayer.workspace.basePaddockLayer

    @property
    def paddockLayer(self):
        return self.featureLayer.workspace.paddockLayer

    def profile(self):
        """Return this Fence's profile."""
        if not self._profile:
            self.recalculate()
        return self._profile

    def getPropertyGeometry(self, glitchBuffer=1.0):
        """Get the property geometry for this Fence."""
        # Get the whole area around the property
        # We are only interested in Paddocks that are going to be there if we Plan this Fence (so Future, not Current)
        # We use the PaddockLayer because it is the reference for Paddock timeframe data
        currentPaddocks = self.paddockLayer.getFeaturesByTimeframe(Timeframe.Future)

        # Get the whole current Paddock area - note the buffering here to reduce glitches
        return QgsGeometry.unaryUnion(p.GEOMETRY.buffer(glitchBuffer, 10) for p in currentPaddocks)
        # return property.buffer(-glitchBuffer, 10)

    def getPropertyNeighbourhood(self):
        """Get the property neighbourhood around this Fence."""
        # Get the whole area around the property
        propertyGeometry = self.getPropertyGeometry()

        if not propertyGeometry or propertyGeometry.isEmpty():
            return None
        propertyExtent = propertyGeometry.boundingBox()
        propertyExtent.scale(1.5)  # Expand by 50%
        return QgsGeometry.fromRect(propertyExtent)

    def getNotPropertyGeometry(self, glitchBuffer=1.0):
        """Get the not property geometry for this Fence."""
        # Get the whole area around the property
        propertyNeighbourhood = self.getPropertyNeighbourhood()
        propertyGeometry = self.getPropertyGeometry(glitchBuffer=glitchBuffer)

        # Get a representation of everything that's not in the property
        notPropertyGeometry = propertyNeighbourhood.difference(propertyGeometry)
        return notPropertyGeometry.buffer(2 * glitchBuffer, 10)

    @Glitch.glitchy()
    def getNewBasePaddocks(self, geometry=None):
        """Get the Base Paddocks that will be newly enclosed by this Fence, and the normalised outer fence lines."""

        fenceLine = geometry or self.GEOMETRY

        if not fenceLine or fenceLine.isEmpty():
            return [], []

        notPropertyGeometry = self.getNotPropertyGeometry(glitchBuffer=1.0)

        if notPropertyGeometry.isEmpty():
            raise Glitch(f"{PLUGIN_NAME} can't find the property boundary, is there any paddock data?")

        if fenceLine.isEmpty():
            return [], []

        # QgsGeometry.fromPolygonXY([g]) to get the rings as polygons
        _, *propertyBoundaries = [QgsGeometry.fromMultiPolylineXY([g]) for g in notPropertyGeometry.asPolygon()]

        # Straightforward case where we have a single new fence line enclosing things
        if fenceLine.isMultipart():
            fenceLine = fenceLine.asGeometryCollection()[0]

        newBasePaddocks = []

        for propertyBoundary in propertyBoundaries:

            intersection = propertyBoundary.intersection(fenceLine)

            if (not intersection.isEmpty()) and intersection.isMultipart():
                # We crossed the not-property boundary more than once, so we are enclosing land
                polyline = fenceLine.asPolyline()
                splitLine = [QgsPointXY(p.x(), p.y()) for p in polyline]

                # qgsDebug("getNewPaddocks: splitGeometry in progress …")
                _, splits, _ = notPropertyGeometry.splitGeometry(splitLine, False)

                # The first result is always the piece of notProperty that is carved out? TODO check this
                if splits:
                    paddockGeometry = notPropertyGeometry.difference(splits[0])
                    newBasePaddock = self.basePaddockLayer.makeFeature()
                    newBasePaddock.draftFeature(paddockGeometry, f"Fence {self.BUILD_ORDER} New")
                    newBasePaddocks.append(newBasePaddock)

        # notPropertyGeometry = self.getNotPropertyGeometry(glitchBuffer=1.0)
        # fenceLine = fenceLine.intersection(notPropertyGeometry)

        if not newBasePaddocks or not fenceLine:
            return [], []
        else:
            return [fenceLine], newBasePaddocks

    @Glitch.glitchy()
    def getCrossedPaddocks(self, geometry=None):
        """Get a tuple representing the restriction of this Fence to only Paddocks it completely crosses,
           and the Paddocks that are completely crossed by the specified line."""

        fenceLine = geometry or self.GEOMETRY

        if not fenceLine or fenceLine.isEmpty():
            return [], []

        # We are only interested in Paddocks that are going to be there if we Plan this Fence (so Future, not Current)
        candidatePaddocks = self.paddockLayer.getFeaturesByTimeframe(Timeframe.Future)

        intersects = [p for p in candidatePaddocks if fenceLine.intersects(p.GEOMETRY)]

        # Crop the fence line to the property
        propertyBoundary = self.getPropertyGeometry(glitchBuffer=1.0)

        # If this makes the fence multipart, we can ignore it
        fenceLine = fenceLine.intersection(propertyBoundary)

        if fenceLine.isEmpty():
            return [], []

        if fenceLine.isMultipart():
            fenceLine = fenceLine.asGeometryCollection()[0]

        # Find the Built paddocks crossed by the fence line that will be superseded
        crossedPaddocks = []
        for paddock in intersects:
            polygon = paddock.GEOMETRY.asMultiPolygon()
            boundaryLine = QgsGeometry.fromMultiPolylineXY(polygon[0])
            intersection = boundaryLine.intersection(fenceLine)
            if intersection.isMultipart():
                crossedPaddocks.append(paddock)

        allCrossed = QgsGeometry.unaryUnion(p.GEOMETRY for p in crossedPaddocks)
        allCrossedBuffered = allCrossed.buffer(1.0, 10)
        fenceLine = fenceLine.intersection(allCrossedBuffered)

        if not crossedPaddocks:
            return [], []
        else:
            return [fenceLine], crossedPaddocks

    def getCrossedBasePaddocks(self, geometry=None):
        """Same as getCrossedPaddocks but returns the crossed Base Paddock features."""
        fenceLines, crossedPaddocks = self.getCrossedPaddocks(geometry)
        return fenceLines, [p.getBasePaddock() for p in crossedPaddocks]

    def _getRelatedPaddocks(self, *statuses):
        """Get the Paddocks with the specified Build Order and group them by STATUS."""
        if self.matchStatus(FeatureStatus.Drafted):
            return self.getCrossedPaddocks(), []

        if self.BUILD_ORDER <= 0:
            raise Glitch(
                "Fence.getCurrentAndFuturePaddocks: BUILD_ORDER must be a positive integer")

        buildFenceRequest = QgsFeatureRequest().setFilterExpression(f'"{BUILD_FENCE}" = {self.BUILD_ORDER}')

        relatedPaddocks = list(self.paddockLayer.getFeatures(request=buildFenceRequest))

        groupedRelatedPaddocks = defaultdict(list)

        for feature in relatedPaddocks:
            for status in statuses:
                if feature.matchStatus(status):
                    groupedRelatedPaddocks[status].append(feature)

        return tuple([groupedRelatedPaddocks[status] for status in statuses])

    def getRelatedPaddocks(self):
        """Get the Paddocks for this Fence."""
        affectedPaddocks, resultingPaddocks = [], []

        if self.matchStatus(FeatureStatus.Drafted):
            _, crossedPaddocks = self.getCrossedPaddocks()
            affectedPaddocks, resultingPaddocks = crossedPaddocks, []
        elif self.matchStatus(FeatureStatus.Planned):
            plannedSupersededPaddocks, builtSupersededPaddocks, plannedPaddocks = self._getRelatedPaddocks(
                FeatureStatus.PlannedSuperseded, FeatureStatus.BuiltSuperseded, FeatureStatus.Planned)
            affectedPaddocks, resultingPaddocks = (plannedSupersededPaddocks + builtSupersededPaddocks), plannedPaddocks
        elif self.matchStatus(FeatureStatus.Built):
            plannedArchivedPaddocks, builtArchivedPaddocks, builtPaddocks = self._getRelatedPaddocks(
                FeatureStatus.PlannedArchived, FeatureStatus.BuiltArchived, FeatureStatus.Built)
            affectedPaddocks, resultingPaddocks = (plannedArchivedPaddocks + builtArchivedPaddocks), builtPaddocks

        affectedPaddocks = [p for p in affectedPaddocks if p.matchTimeframe(Timeframe.Current)]
        resultingPaddocks = [p for p in resultingPaddocks if p.matchTimeframe(Timeframe.Future)]

        qgsDebug(f"Affected paddocks = {str([format(p) for p in affectedPaddocks])}")
        qgsDebug(f"Resulting paddocks = {str([format(p) for p in resultingPaddocks])}")

        return affectedPaddocks, resultingPaddocks

    @FeatureAction.draft.handleAndPersist()
    def draftFeature(self, geometry):
        """Draft a Fence."""

        self.GEOMETRY = geometry

        edits = Edits()

        # New Paddocks
        enclosingLines, newPaddocks = self.getNewBasePaddocks()

        # qgsDebug(
        # f"Fence.draftFeature getNewPaddocks {len(enclosingLines)},
        # {len(newPaddocks)}, {[p.NAME for p in newPaddocks]}")

        # Split Paddocks
        splitLines, supersededPaddocks = self.getCrossedBasePaddocks()

        # qgsDebug(
        # f"Fence.draftFeature getCrossedPaddocks {len(splitLines)},
        # {len(supersededPaddocks)}, {[p.NAME for p in supersededPaddocks]}")

        fenceLines = enclosingLines + splitLines

        if (not newPaddocks and not supersededPaddocks) or not fenceLines:
            # qgsDebug("Fence.draftFeature: no new or superseded Paddocks, returning")
            return Edits.delete(self)
            # raise Glitch("The specified Fence does not cross or touch any Built or
            # Planned Paddocks, or enclose any new Paddocks.")

        self.GEOMETRY, *fenceLines = fenceLines

        for fenceLine in fenceLines:
            extraFence = self.featureLayer.makeFeature()
            edits = edits.editAfter(extraFence.draftFeature(fenceLine))

        currentBuildOrder, _, _ = self.featureLayer.getBuildOrder()
        self.BUILD_ORDER = currentBuildOrder + 1

        return Edits.upsert(self).editBefore(edits)

    @FeatureAction.plan.handleAndPersist()
    def planFeature(self):
        """Plan the Paddocks that would be altered after building this Fence."""

        edits = Edits()

        with Edits.editAndRollBack([self.basePaddockLayer]):

            _, lowestDraftBuildOrder, _ = self.featureLayer.getBuildOrder()

            if self.BUILD_ORDER > lowestDraftBuildOrder:
                raise Glitch(
                    "You must Plan your Drafted Fences from first to last according to Build Order.")

            if self.BUILD_ORDER <= 0:
                raise Glitch("Fence must have a positive Build Order to be Planned")

            _, crossedBasePaddocks = self.getCrossedBasePaddocks()

            fenceLine = self.GEOMETRY
            polyline = fenceLine.asPolyline()
            points = [QgsPoint(p.x(), p.y()) for p in polyline]
            splitLine = QgsLineString(points)

            self.basePaddockLayer.splitFeatures(splitLine, False, False)

            futurePaddocksAfterSplit = self.basePaddockLayer.getFeaturesByTimeframe(Timeframe.Future)

            for crossedPaddock in crossedBasePaddocks:
                crossedPaddockName = crossedPaddock.NAME

                # Deep copy all split paddocks based on NAME, which is preserved
                splitPaddocks = [self.basePaddockLayer.copyFeature(f)
                                 for f in futurePaddocksAfterSplit
                                 if f.NAME == crossedPaddockName]

                for i, splitPaddock in enumerate(splitPaddocks):
                    defaultName = crossedPaddockName + ' ' + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]
                    splitPaddock.NAME = defaultName
                    # Note this is set explicitly to Drafted because
                    # the Paddock is derived in a dodgy way using splitFeatures
                    splitPaddock.STATUS = FeatureStatus.Drafted
                    splitPaddock.recalculate()
                    edits.editBefore(splitPaddock.planFeature(self, crossedPaddock))

        _, newBasePaddocks = self.getNewBasePaddocks()

        # qgsDebug(f"Fence.planFeature: getNewPaddocks {len(newPaddocks)}, {[p.NAME for p in newPaddocks]}")

        for paddock in newBasePaddocks:
            edits.editBefore(paddock.planFeature(self))

        _, crossedBasePaddocks = self.getCrossedBasePaddocks()

        # qgsDebug(f"Fence.planFeature: getCrossedPaddocks {len(supersededPaddocks)}, {[p.NAME for p in supersededPaddocks]}")

        for paddock in crossedBasePaddocks:
            edits.editBefore(paddock.supersedeFeature(self))

        # self.basePaddockLayer now rolls back
        return Edits.upsert(self).editAfter(edits)

    @FeatureAction.undoPlan.handleAndPersist()
    def undoPlanFeature(self):
        """Undo the plan of Paddocks implied by a Fence."""

        edits = Edits()

        supersededPaddocks, plannedPaddocks = self.getRelatedPaddocks()

        for supersededPaddock in supersededPaddocks:
            edits = edits.editBefore(supersededPaddock.undoSupersedeFeature())

        for plannedPaddock in plannedPaddocks:
            edits = edits.editBefore(plannedPaddock.undoPlanFeature())

        return Edits.upsert(self).editAfter(edits)

    @FeatureAction.build.handleAndPersist()
    def buildFeature(self):
        """Undo the plan of Paddocks implied by a Fence."""

        edits = Edits()

        supersededPaddocks, plannedPaddocks = self.getRelatedPaddocks()

        for supersededPaddock in supersededPaddocks:
            edits = edits.editBefore(supersededPaddock.archiveFeature())

        # # qgsDebug(f"Fence.buildFeature after archive Paddock processing: {edits.upserts}")

        for plannedPaddock in plannedPaddocks:
            edits = edits.editBefore(plannedPaddock.buildFeature())

        # # qgsDebug(f"Fence.buildFeature after build Paddock processing: {edits.upserts}")

        return Edits.upsert(self).editAfter(edits)

        # qgsDebug(f"Fence.buildFeature after build Paddock processing: {edits.upserts}")

    @FeatureAction.undoBuild.handleAndPersist()
    def undoBuildFeature(self):
        """Undo the plan of Paddocks implied by a Fence."""

        edits = Edits()

        archivedPaddocks, builtPaddocks = self.getRelatedPaddocks()

        for archivedPaddock in archivedPaddocks:
            edits = edits.editBefore(archivedPaddock.undoArchiveFeature())

        for builtPaddock in builtPaddocks:
            edits = edits.editBefore(builtPaddock.undoBuildFeature())

        return Edits.upsert(self).editAfter(edits)
