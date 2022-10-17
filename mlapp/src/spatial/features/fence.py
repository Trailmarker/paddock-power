# -*- coding: utf-8 -*-
from qgis.core import QgsFeatureRequest, QgsGeometry, QgsLineString, QgsPoint

from ...models.paddock_power_error import PaddockPowerError
from ...utils import qgsDebug
from ..layers.edit_context import editAndRollBack
from ..layers.elevation_layer import ElevationLayer
from ..layers.paddock_layer import PaddockLayer
from .feature_status import FeatureStatus
from .line_feature import LineFeature
from .schemas import FenceSchema, addSchema, BUILD_FENCE


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

    def getCrossedPaddocks(self):
        """Get a tuple representing the restriction of this Fence to only Paddocks it completely crosses,
           and the Paddocks that are completely crossed by the specified line."""

        fenceLine = self.geometry()

        # We are only interested in Paddocks that are current
        existingAndPlannedPaddocks = self.paddockLayer.getFeaturesByStatus(
            FeatureStatus.Existing, FeatureStatus.Planned)

        intersects = [p for p in existingAndPlannedPaddocks if fenceLine.intersects(p.geometry())]

        # qgsDebug(f"[p.name for p in intersects] = {[p.name() for p in intersects]}")

        # Find the existing paddocks crossed by the fence line that will be superseded
        crossedPaddocks = []
        for paddock in intersects:
            polygon = paddock.geometry().asMultiPolygon()
            boundaryLine = QgsGeometry.fromMultiPolylineXY(polygon[0])
            intersection = boundaryLine.intersection(fenceLine)
            if intersection.isMultipart():
                # qgsDebug("Found a fully crossed paddock")
                # Deep copy the crossed paddocks
                crossedPaddocks.append(self.paddockLayer.makeFeature(paddock))

        # qgsDebug(f"[p.name for p in crossedPaddocks] = {[p.name() for p in crossedPaddocks]}")

        # Crop the fence line to these superseded paddocks - no loose ends
        allCrossed = QgsGeometry.unaryUnion(
            f.geometry() for f in crossedPaddocks)
        allCrossedBuffered = allCrossed.buffer(5.0, 10)
        normalisedFenceLine = fenceLine.intersection(allCrossedBuffered)

        if normalisedFenceLine.isEmpty():
            # qgsDebug("getCrossedPaddocks: normalisedFenceLine is empty")
            return normalisedFenceLine, []

        # If this leaves the fence line multipart, reduce it to a single part
        if normalisedFenceLine.isMultipart():
            # qgsDebug("getCrossedPaddocks: normalisedFenceLine is multipart")
            normalisedFenceLine = normalisedFenceLine.combine()

        if normalisedFenceLine.isMultipart():
            raise PaddockPowerError(
                "Fence.analyseFence: fence line is still multipart")

        return normalisedFenceLine, crossedPaddocks

    def draftFence(self):
        """Draft a Fence."""

        self.draft.emit()

        try:
            currentBuildOrder, _, _ = self.featureLayer.getBuildOrder()

            normalisedFenceLine, supersededPaddocks = self.getCrossedPaddocks()

            if normalisedFenceLine is None or normalisedFenceLine.isEmpty() or not supersededPaddocks:
                raise PaddockPowerError("The specified Fence does not cross or touch any Paddocks.")

            self.setGeometry(normalisedFenceLine)
            self.buildOrder = currentBuildOrder + 1
            self.recalculate()
            self.upsert()
        except BaseException:
            self.undoDraft.emit()
            raise


    def onPlan(self):
        """Plan the Paddocks that would be altered after building this Fence."""
        qgsDebug(f"Fence.onPlan: {self._debugStateMachine()}")

        self._supersededPaddocks = []
        self._plannedPaddocks = []

        with editAndRollBack(self.paddockLayer):
        
            _, lowestDraftBuildOrder, _ = self.featureLayer.getBuildOrder()

            if self.buildOrder > lowestDraftBuildOrder:
                raise PaddockPowerError(
                    "You must Plan your Drafted Fences from first to last according to Build Order.")

            if self.buildOrder <= 0:
                raise PaddockPowerError("Fence must have a positive Build Order to be Planned")

            _, supersededPaddocks = self.getCrossedPaddocks()

            fenceLine = self.geometry()
            polyline = fenceLine.asPolyline()
            points = [QgsPoint(p.x(), p.y()) for p in polyline]
            splitLine = QgsLineString(points)

            self.paddockLayer.splitFeatures(splitLine, False, False)

            existingAndPlannedPaddocks = self.paddockLayer.getFeaturesByStatus(
                FeatureStatus.Existing, FeatureStatus.Planned)

            plannedPaddocks = []

            for crossedPaddock in supersededPaddocks:
                crossedPaddockName = crossedPaddock.name

                # Derive the split paddocks
                splitPaddocks = [f for f in existingAndPlannedPaddocks
                                 if f.name == crossedPaddockName]

                for i, splitPaddock in enumerate(splitPaddocks):
                    # If this is one of the 'crossed' paddocks after the split, add, don't update
                    creatingNewPaddock = splitPaddock.id() == crossedPaddock.id()

                    if creatingNewPaddock:
                        # Try to create an entirely new Paddock feature
                        # Conflicts get quite weird here
                        splitPaddock = self.paddockLayer.copyFeature(splitPaddock)

                    defaultName = crossedPaddockName + ' ' + \
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]

                    splitPaddock.name = defaultName
                    splitPaddock.planPaddock(self)
                    plannedPaddocks.append(splitPaddock)

            for paddock in supersededPaddocks:
                paddock.supersedePaddock(self)

            self._supersededPaddocks, self._plannedPaddocks = supersededPaddocks, plannedPaddocks


        self.featuresProcessed.emit([self] + self._supersededPaddocks + self._plannedPaddocks)

    


    def undoPlanFence(self):
        """Undo the plan of Paddocks implied by a Fence."""

        qgsDebug(f"Fence.undoPlanFence: {self._debugStateMachine()}")

        # self.calculateSupersededAndPlannedPaddocks()

        #qgsDebug(f"self._supersededPaddocks = {self._supersededPaddocks}")

        self.undoPlan.emit()

        qgsDebug(f"Fence.undoPlanFence after undoPlan.emit(): {self._debugStateMachine()}")

        # for paddock in self.supersededPaddocks():
        #     # Could be a few issues here …
        #     paddock.undoSupersedePaddock(self)
        #     paddock.upsert(paddock)

        # for paddock in self.plannedPaddocks():
        #     paddock.delete()

        self.upsert()

    def calculateSupersededAndPlannedPaddocks(self):
        """Get the Paddocks with the specified Build Order."""

        if self.status == FeatureStatus.Drafted:
            _, self._supersededPaddocks = self.getCrossedPaddocks()
            self._plannedPaddocks = []
            return

        buildOrder = self.buildOrder

        if buildOrder <= 0:
            raise PaddockPowerError(
                "Fence.getSupersededAndPlannedPaddocks: buildOrder must be a positive integer")

        buildFenceRequest = QgsFeatureRequest().setFilterExpression(f'"{BUILD_FENCE}" = {buildOrder}')

        paddocks = list(self.paddockLayer.getFeatures(request=buildFenceRequest))

        self._supersededPaddocks = [
            f for f in paddocks if f.status in [
                FeatureStatus.PlannedSuperseded,
                FeatureStatus.ExistingSuperseded]]
        self._plannedPaddocks = [f for f in paddocks if f.status == FeatureStatus.Planned]

    def recalculate(self):
        """Recalculate both profile data and the related Paddocks."""
        super().recalculate()
        self.calculateSupersededAndPlannedPaddocks()

    def supersededPaddocks(self):
        """Return a list of paddocks that will be or have been Superseded by this Fence."""
        return self._supersededPaddocks

    def plannedPaddocks(self):
        """Return a list of paddocks that will be or have been Planned by this Fence."""
        return self._plannedPaddocks
