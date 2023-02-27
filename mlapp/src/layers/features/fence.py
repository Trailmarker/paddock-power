# -*- coding: utf-8 -*-
from shapely.geometry import shape
from shapely.ops import split

from qgis.core import QgsGeometry
from collections import defaultdict
from qgis.core import QgsFeatureRequest, QgsGeometry

from ...models import Glitch
from ...utils import PLUGIN_NAME, qgsInfo
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

    def getNewBasePaddocks(self):
        """Get the Base Paddocks that will be newly enclosed by this Fence, and the normalised outer fence lines."""

        fenceLine = self.GEOMETRY

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
                blade = shape(fenceLine.__geo_interface__)

                notPropertyGeometry = shape(self.getNotPropertyGeometry().__geo_interface__)
                splits = split(notPropertyGeometry, blade)

                # The first result is always the piece of notProperty that is carved out? TODO check this
                if splits:
                    paddockGeometry = notPropertyGeometry.difference(splits[0])
                    newBasePaddock = self.basePaddockLayer.makeFeature()
                    newBasePaddock.draftFeature(QgsGeometry.fromWkt(paddockGeometry.wkt))
                    newBasePaddocks.append(newBasePaddock)

        # notPropertyGeometry = self.getNotPropertyGeometry(glitchBuffer=1.0)
        # fenceLine = fenceLine.intersection(notPropertyGeometry)

        if not newBasePaddocks or not fenceLine:
            return [], []
        else:
            return [fenceLine], newBasePaddocks

    def getCrossedPaddocks(self):
        """Get a tuple representing the restriction of this Fence to only Paddocks it completely crosses,
           and the Paddocks that are completely crossed by the specified line."""

        fenceLine = self.GEOMETRY

        if not fenceLine or fenceLine.isEmpty():
            return [], []

        # We are only interested in Paddocks that are going to be there if we Plan this Fence (so Future, not Current)
        candidatePaddocks = self.paddockLayer.getFeaturesByTimeframe(
            Timeframe.Future,
            QgsFeatureRequest().setFilterRect(fenceLine.boundingBox()))

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
            # Set up again, but with the attributes
            return [fenceLine], crossedPaddocks

    def getCrossedBasePaddocks(self):
        """Same as getCrossedPaddocks but returns the crossed Base Paddock features."""
        fenceLines, crossedPaddocks = self.getCrossedPaddocks()
        return fenceLines, [f for f in self.basePaddockLayer.getFeatures(
            QgsFeatureRequest().setFilterFids([p.PADDOCK for p in crossedPaddocks]))]

    def _getRelatedPaddocks(self, *statuses):
        """Get the Paddocks with the specified Build Order and group them by STATUS."""
        if self.matchStatus(FeatureStatus.Drafted):
            return self.getCrossedPaddocks(), []

        if self.BUILD_ORDER <= 0:
            raise Glitch(
                "Fence.getCurrentAndFuturePaddocks: BUILD_ORDER must be a positive integer")

        buildFenceRequest = QgsFeatureRequest().setFilterExpression(f'"{BUILD_FENCE}" = {self.BUILD_ORDER}')

        relatedPaddocks = self.paddockLayer.getFeatures(request=buildFenceRequest)

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

        # qgsDebug(f"Affected paddocks = {str([format(p) for p in affectedPaddocks])}")
        # qgsDebug(f"Resulting paddocks = {str([format(p) for p in resultingPaddocks])}")

        return affectedPaddocks, resultingPaddocks

    @FeatureAction.draft.handleWithSave()
    def draftFeature(self, geometry):
        """Draft a Fence."""

        self.GEOMETRY = geometry

        edits = Edits()

        # New Paddocks
        enclosingLines, newPaddocks = self.getNewBasePaddocks()

        # Split Paddocks
        splitLines, supersededPaddocks = self.getCrossedBasePaddocks()

        fenceLines = enclosingLines + splitLines

        if (not newPaddocks and not supersededPaddocks) or not fenceLines:
            qgsInfo("The sketched Fence did not cross or touch any Built or Planned Paddocks, or enclose any new Paddocks.")
            return Edits.delete(self)

        self.GEOMETRY, *fenceLines = fenceLines

        for fenceLine in fenceLines:
            extraFence = self.featureLayer.makeFeature()
            edits = edits.editAfter(extraFence.draftFeature(fenceLine))

        currentBuildOrder, _, _ = self.featureLayer.getBuildOrder()
        self.BUILD_ORDER = currentBuildOrder + 1

        return Edits.upsert(self).editBefore(edits)

    @FeatureAction.plan.handleWithSave()
    def planFeature(self):
        """Plan the Paddocks that would be altered after building this Fence."""

        _, lowestDraftBuildOrder, _ = self.featureLayer.getBuildOrder()

        if self.BUILD_ORDER > lowestDraftBuildOrder:
            raise Glitch(
                "You must Plan your Drafted Fences from first to last according to Build Order.")

        if self.BUILD_ORDER <= 0:
            raise Glitch("Fence must have a positive Build Order to be Planned")

        _, crossedBasePaddocks = self.getCrossedBasePaddocks()

        fenceLine = self.GEOMETRY
        blade = shape(fenceLine.__geo_interface__)
        edits = Edits()

        for crossedBasePaddock in crossedBasePaddocks:
            crossedPaddockGeometry = shape(crossedBasePaddock.GEOMETRY.__geo_interface__)
            splits = split(crossedPaddockGeometry, blade)

            for i, splitGeometry in enumerate(splits):
                splitPaddock = self.basePaddockLayer.makeFeature()

                splitPaddock.draftFeature(
                    QgsGeometry.fromWkt(splitGeometry.wkt),
                    crossedBasePaddock.NAME + ' ' + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i])

                splitPaddock.recalculate()
                edits.editBefore(splitPaddock.planFeature(self, crossedBasePaddock))

        _, newBasePaddocks = self.getNewBasePaddocks()

        for paddock in newBasePaddocks:
            edits.editBefore(paddock.planFeature(self))

        for crossedBasePaddock in crossedBasePaddocks:
            edits.editBefore(crossedBasePaddock.supersedeFeature(self))

        return Edits.upsert(self).editAfter(edits)

    @FeatureAction.undoPlan.handleWithSave()
    def undoPlanFeature(self):
        """Undo the plan of Paddocks implied by a Fence."""

        edits = Edits()

        supersededPaddocks, plannedPaddocks = self.getRelatedPaddocks()

        for supersededPaddock in supersededPaddocks:
            edits = edits.editBefore(supersededPaddock.undoSupersedeFeature())

        for plannedPaddock in plannedPaddocks:
            edits = edits.editBefore(plannedPaddock.undoPlanFeature())

        return Edits.upsert(self).editAfter(edits)

    @FeatureAction.build.handleWithSave()
    def buildFeature(self):
        """Undo the plan of Paddocks implied by a Fence."""

        edits = Edits()

        supersededPaddocks, plannedPaddocks = self.getRelatedPaddocks()

        for supersededPaddock in supersededPaddocks:
            edits = edits.editBefore(supersededPaddock.archiveFeature())

        # qgsDebug(f"Fence.buildFeature after archive Paddock processing: {edits.upserts}")

        for plannedPaddock in plannedPaddocks:
            edits = edits.editBefore(plannedPaddock.buildFeature())

        # qgsDebug(f"Fence.buildFeature after build Paddock processing: {edits.upserts}")

        return Edits.upsert(self).editAfter(edits)

        # qgsDebug(f"Fence.buildFeature after build Paddock processing: {edits.upserts}")

    @FeatureAction.undoBuild.handleWithSave()
    def undoBuildFeature(self):
        """Undo the plan of Paddocks implied by a Fence."""

        edits = Edits()

        archivedPaddocks, builtPaddocks = self.getRelatedPaddocks()

        for archivedPaddock in archivedPaddocks:
            edits = edits.editBefore(archivedPaddock.undoArchiveFeature())

        for builtPaddock in builtPaddocks:
            edits = edits.editBefore(builtPaddock.undoBuildFeature())

        return Edits.upsert(self).editAfter(edits)
