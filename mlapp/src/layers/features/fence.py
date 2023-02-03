# -*- coding: utf-8 -*-
from qgis.core import QgsFeatureRequest, QgsGeometry, QgsLineString, QgsPoint, QgsProject, QgsPointXY, QgsRectangle

from ...models import Glitch
from ...utils import PLUGIN_NAME
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
    def paddockLayer(self):
        return self.featureLayer.workspace.paddockLayer

    @property
    def metricPaddockLayer(self):
        return self.featureLayer.workspace.metricPaddockLayer

    @property
    def isInfrastructure(self):
        """Return True for Fence."""
        return True

    def profile(self):
        """Return this Fence's profile."""
        if not self._profile:
            self.recalculate()
        return self._profile

    def getPropertyGeometry(self, glitchBuffer=1.0):
        """Get the property geometry for this Fence."""
        # Get the whole area around the property
        # We are only interested in Paddocks that are current
        currentPaddocks = self.paddockLayer.getFeaturesByTimeframe(Timeframe.Future)

        # Get the whole current Paddock area - note the buffering here to reduce glitches
        return QgsGeometry.unaryUnion(p.GEOMETRY.buffer(glitchBuffer, 10) for p in currentPaddocks)
        # return property.buffer(-glitchBuffer, 10)

    def getPropertyNeighbourhood(self):
        """Get the property neighbourhood around this Fence."""
        # Get the whole area around the property
        propertyExtent = QgsRectangle(self.paddockLayer.extent())
        propertyExtent.scale(1.5)  # Expand by 50%
        return QgsGeometry.fromRect(propertyExtent)

    def getNotPropertyGeometry(self, glitchBuffer=1.0):
        """Get the not property geometry for this Fence."""
        # Get the whole area around the property
        propertyRegion = self.getPropertyNeighbourhood()
        propertyGeometry = self.getPropertyGeometry(glitchBuffer=glitchBuffer)

        # Get a representation of everything that's not in the property
        notPropertyGeometry = propertyRegion.difference(propertyGeometry)
        return notPropertyGeometry.buffer(2 * glitchBuffer, 10)

    @Glitch.glitchy()
    def getNewPaddocks(self, geometry=None):
        """Get the paddocks that are newly enclosed by this Fence, and the normalised outer fence lines."""

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

        newPaddocks = []

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
                    newPaddock = self.paddockLayer.makeFeature()
                    newPaddock.draftFeature(paddockGeometry, f"Fence {self.BUILD_ORDER} New")
                    newPaddocks.append(newPaddock)

        # notPropertyGeometry = self.getNotPropertyGeometry(glitchBuffer=1.0)
        # fenceLine = fenceLine.intersection(notPropertyGeometry)

        if not newPaddocks or not fenceLine:
            return [], []
        else:
            return [fenceLine], newPaddocks

    @Glitch.glitchy()
    def getCrossedPaddocks(self, geometry=None):
        """Get a tuple representing the restriction of this Fence to only Paddocks it completely crosses,
           and the Paddocks that are completely crossed by the specified line."""

        fenceLine = geometry or self.GEOMETRY

        if not fenceLine or fenceLine.isEmpty():
            return [], []

        # We are only interested in Paddocks that are current
        currentPaddocks = self.paddockLayer.getFeaturesByTimeframe(Timeframe.Future)

        intersects = [p for p in currentPaddocks if fenceLine.intersects(p.GEOMETRY)]

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

    def getPaddocks(self):
        """Get the MetricPaddocks with the specified Build Order."""
        if self.STATUS == FeatureStatus.Drafted:
            return [], []
            # _, crossedPaddocks = self.getCrossedPaddocks()
            # return crossedPaddocks, []

        if self.BUILD_ORDER <= 0:
            raise Glitch(
                "Fence.getCurrentAndFuturePaddocks: BUILD_ORDER must be a positive integer")

        buildFenceRequest = QgsFeatureRequest().setFilterExpression(f'"{BUILD_FENCE}" = {self.BUILD_ORDER}')

        return list(self.metricPaddockLayer.getFeatures(request=buildFenceRequest))

    def getCurrentAndFuturePaddocks(self):
        """Get the MetricPaddocks with the specified Build Order."""

        metricPaddocks = self.getPaddocks()

        return ([feature for feature in metricPaddocks if feature.TIMEFRAME.matchTimeframe(Timeframe.Current)],
                [feature for feature in metricPaddocks if feature.TIMEFRAME.matchTimeframe(Timeframe.Future)])

    @Edits.persistFeatures
    @FeatureAction.draft.handler()
    def draftFeature(self, geometry):
        """Draft a Fence."""

        self.GEOMETRY = geometry

        edits = Edits()

        # New Paddocks
        enclosingLines, newPaddocks = self.getNewPaddocks()

        # qgsDebug(
        # f"Fence.draftFeature getNewPaddocks {len(enclosingLines)},
        # {len(newPaddocks)}, {[p.NAME for p in newPaddocks]}")

        # Split Paddocks
        splitLines, supersededPaddocks = self.getCrossedPaddocks()

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

    @Edits.persistFeatures
    @FeatureAction.plan.handler()
    def planFeature(self):
        """Plan the Paddocks that would be altered after building this Fence."""

        edits = Edits()

        with Edits.editAndRollBack([self.paddockLayer]):

            _, lowestDraftBuildOrder, _ = self.featureLayer.getBuildOrder()

            if self.BUILD_ORDER > lowestDraftBuildOrder:
                raise Glitch(
                    "You must Plan your Drafted Fences from first to last according to Build Order.")

            if self.BUILD_ORDER <= 0:
                raise Glitch("Fence must have a positive Build Order to be Planned")

            _, supersededPaddocks = self.getCrossedPaddocks()

            fenceLine = self.GEOMETRY
            polyline = fenceLine.asPolyline()
            points = [QgsPoint(p.x(), p.y()) for p in polyline]
            splitLine = QgsLineString(points)

            self.paddockLayer.splitFeatures(splitLine, False, False)

            currentPaddocks = self.paddockLayer.getFeaturesByTimeframe(Timeframe.Future)

            for crossedPaddock in supersededPaddocks:
                crossedPaddockName = crossedPaddock.NAME

                # Deep copy all split paddocks
                splitPaddocks = [self.paddockLayer.copyFeature(f)
                                 for f in currentPaddocks
                                 if f.NAME == crossedPaddockName]

                for i, splitPaddock in enumerate(splitPaddocks):
                    defaultName = crossedPaddockName + ' ' + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]
                    splitPaddock.NAME = defaultName
                    # Note this is set explicitly to Drafted because
                    # the Paddock is derived in a dodgy way using splitFeatures
                    splitPaddock.STATUS = FeatureStatus.Drafted
                    splitPaddock.recalculate()
                    edits.editBefore(splitPaddock.planFeature(self, crossedPaddock))

        _, newPaddocks = self.getNewPaddocks()

        # qgsDebug(f"Fence.planFeature: getNewPaddocks {len(newPaddocks)}, {[p.NAME for p in newPaddocks]}")

        for paddock in newPaddocks:
            edits.editBefore(paddock.planFeature(self))

        _, supersededPaddocks = self.getCrossedPaddocks()

        # qgsDebug(f"Fence.planFeature: getCrossedPaddocks {len(supersededPaddocks)}, {[p.NAME for p in supersededPaddocks]}")

        for paddock in supersededPaddocks:
            edits.editBefore(paddock.supersedeFeature(self))

        # self.paddockLayer now rolls back
        return Edits.upsert(self).editAfter(edits)

    @Edits.persistFeatures
    @FeatureAction.plan.handler()
    def planFeature(self):
        """Plan the Paddocks that would be altered after building this Fence."""

        edits = Edits()

        with Edits.editAndRollBack([self.paddockLayer]):

            _, lowestDraftBuildOrder, _ = self.featureLayer.getBuildOrder()

            if self.BUILD_ORDER > lowestDraftBuildOrder:
                raise Glitch(
                    "You must Plan your Drafted Fences from first to last according to Build Order.")

            if self.BUILD_ORDER <= 0:
                raise Glitch("Fence must have a positive Build Order to be Planned")

            _, supersededPaddocks = self.getCrossedPaddocks()

            fenceLine = self.GEOMETRY
            polyline = fenceLine.asPolyline()
            points = [QgsPoint(p.x(), p.y()) for p in polyline]
            splitLine = QgsLineString(points)

            self.paddockLayer.splitFeatures(splitLine, False, False)

            currentPaddocks = self.paddockLayer.getFeaturesByTimeframe(Timeframe.Future)

            for crossedPaddock in supersededPaddocks:
                crossedPaddockName = crossedPaddock.NAME

                # Deep copy all split paddocks
                splitPaddocks = [self.paddockLayer.copyFeature(f)
                                 for f in currentPaddocks
                                 if f.NAME == crossedPaddockName]

                for i, splitPaddock in enumerate(splitPaddocks):
                    defaultName = crossedPaddockName + ' ' + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]
                    splitPaddock.NAME = defaultName
                    # Note this is set explicitly to Drafted because
                    # the Paddock is derived in a dodgy way using splitFeatures
                    splitPaddock.STATUS = FeatureStatus.Drafted
                    splitPaddock.recalculate()
                    edits.editBefore(splitPaddock.planFeature(self, crossedPaddock))

        _, newPaddocks = self.getNewPaddocks()

        # qgsDebug(f"Fence.planFeature: getNewPaddocks {len(newPaddocks)}, {[p.NAME for p in newPaddocks]}")

        for paddock in newPaddocks:
            edits.editBefore(paddock.planFeature(self))

        _, supersededPaddocks = self.getCrossedPaddocks()

        # qgsDebug(f"Fence.planFeature: getCrossedPaddocks {len(supersededPaddocks)}, {[p.NAME for p in supersededPaddocks]}")

        for paddock in supersededPaddocks:
            edits.editBefore(paddock.supersedeFeature(self))

        # self.paddockLayer now rolls back
        return Edits.upsert(self).editAfter(edits)

    @Edits.persistFeatures
    @FeatureAction.undoPlan.handler()
    def undoPlanFeature(self):
        """Undo the plan of Paddocks implied by a Fence."""

        edits = Edits()

        supersededPaddocks, plannedPaddocks = self.getCurrentAndFuturePaddocks()

        # qgsDebug(f"supersededPaddocks = {str(supersededPaddocks)}")
        # qgsDebug(f"plannedPaddocks = {str(plannedPaddocks)}")

        for metricPaddock in supersededPaddocks:
            edits = edits.editBefore(metricPaddock.undoSupersedeFeature())

        for metricPaddock in plannedPaddocks:
            edits = edits.editBefore(metricPaddock.undoPlanFeature())

        return Edits.upsert(self).editAfter(edits)

    @Edits.persistFeatures
    @FeatureAction.build.handler()
    def buildFeature(self):
        """Undo the plan of Paddocks implied by a Fence."""

        edits = Edits()

        supersededPaddocks, plannedPaddocks = self.getCurrentAndFuturePaddocks()

        for metricPaddock in supersededPaddocks:
            edits = edits.editBefore(metricPaddock.archiveFeature())

        for metricPaddock in plannedPaddocks:
            edits = edits.editBefore(metricPaddock.buildFeature())

        return Edits.upsert(self).editAfter(edits)

    @Edits.persistFeatures
    @FeatureAction.undoBuild.handler()
    def buildFeature(self):
        """Undo the plan of Paddocks implied by a Fence."""

        edits = Edits()

        paddocks = self.getPaddocks()
        
        builtPaddocks = [p for p in paddocks if p.STATUS.name == FeatureStatus.Built.name]
        archivedPaddocks = [p for p in paddocks if p.STATUS.name == FeatureStatus.Archived.name]

        for metricPaddock in builtPaddocks:
            edits = edits.editBefore(metricPaddock.undoBuildFeature())

        for metricPaddock in archivedPaddocks:
            edits = edits.editBefore(metricPaddock.undoArchiveFeature())

        return Edits.upsert(self).editAfter(edits)