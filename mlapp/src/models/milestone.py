# -*- coding: utf-8 -*-
from os import path

import processing

from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.core import QgsFeature, QgsProject
from qgis.utils import iface

from ..spatial.feature.feature_status import FeatureStatus
from ..spatial.feature.fence import Fence
from ..spatial.feature.paddock import Paddock
from ..spatial.feature.pipeline import Pipeline
from ..spatial.layer.boundary_layer import BoundaryLayer
from ..spatial.layer.fence_layer import FenceLayer
from ..spatial.layer.paddock_layer import PaddockLayer
from ..spatial.layer.paddock_power_vector_layer import PaddockPowerLayerSourceType
from ..spatial.layer.pipeline_layer import PipelineLayer
from ..spatial.layer.waterpoint_layer import WaterpointLayer
from ..utils import guiError

from ..widgets.paddock_power_map_tool import PaddockPowerMapTool

from .paddock_power_error import PaddockPowerError


class Milestone(QObject):
    # emit this signal when paddocks are updated
    selectedFenceChanged = pyqtSignal(QgsFeature)
    selectedPaddockChanged = pyqtSignal(QgsFeature)
    selectedPipelineChanged = pyqtSignal(QgsFeature)
    milestoneDataChanged = pyqtSignal()

    def __init__(self, milestoneName, gpkgFile):
        super(Milestone, self).__init__()

        self.milestoneName = milestoneName
        self.gpkgFile = gpkgFile
        self.currentTool = None
        self.isLoaded = False

        self.selectedFence = None
        self.selectedPaddock = None
        self.selectedPipeline = None

    def create(self):
        """Create this milestone in its GeoPackage."""
        # TODO these are not consistent
        # Create paddocks, pipeline, fence, waterpoints, boundary layers
        boundary = BoundaryLayer(layerName=f"{self.milestoneName} Boundary")
        waterpoint = WaterpointLayer(
            layerName=f"{self.milestoneName} Waterpoints")
        pipeline = PipelineLayer(layerName=f"{self.milestoneName} Pipeline")
        fence = FenceLayer(layerName=f"{self.milestoneName} Fence")
        paddock = PaddockLayer(layerName=f"{self.milestoneName} Paddocks")

        # The 'Layers' parameter of the Package Layers tool ('native:package')
        # Note this is sensitive to order
        layers = [boundary, waterpoint, pipeline, fence, paddock]

        # Add milestone to GeoPackage using the Package Layers tool
        params = {
            'LAYERS': layers,
            # 'OUTPUT': parameters['ProjectName'],
            'OVERWRITE': not path.exists(self.gpkgFile),
            'SAVE_STYLES': False,
            'OUTPUT': self.gpkgFile
        }

        processing.run(
            'native:package', params)

        # Load the required layers for this milestone from the source
        self.load()

    def load(self):
        """Load this milestone its GeoPackage."""
        boundaryLayerName = f"{self.milestoneName} Boundary"
        self.boundaryLayer = BoundaryLayer(sourceType=PaddockPowerLayerSourceType.File,
                                           layerName=boundaryLayerName, gpkgFile=self.gpkgFile)
        waterpointLayerName = f"{self.milestoneName} Waterpoints"
        self.waterpointLayer = WaterpointLayer(sourceType=PaddockPowerLayerSourceType.File,
                                               layerName=waterpointLayerName, gpkgFile=self.gpkgFile)
        pipelineLayerName = f"{self.milestoneName} Pipeline"
        self.pipelineLayer = PipelineLayer(sourceType=PaddockPowerLayerSourceType.File,
                                           layerName=pipelineLayerName, gpkgFile=self.gpkgFile)
        fenceLayerName = f"{self.milestoneName} Fence"
        self.fenceLayer = FenceLayer(sourceType=PaddockPowerLayerSourceType.File,
                                     layerName=fenceLayerName, gpkgFile=self.gpkgFile)
        paddockLayerName = f"{self.milestoneName} Paddocks"
        self.paddockLayer = PaddockLayer(sourceType=PaddockPowerLayerSourceType.File,
                                         layerName=paddockLayerName, gpkgFile=self.gpkgFile)

        # TODO hacky
        self.fenceLayer.featureAdded.connect(
            lambda: self.milestoneDataChanged.emit())
        self.paddockLayer.featureAdded.connect(
            lambda: self.milestoneDataChanged.emit())

        self.isLoaded = True

    def findGroup(self):
        """Find this milestone's group in the Layers panel."""
        return QgsProject.instance().layerTreeRoot().findGroup(self.milestoneName)

    def addToMap(self):
        """Add this milestone to the current map view."""
        group = self.findGroup()
        if group is None:
            group = QgsProject.instance().layerTreeRoot().insertGroup(0, self.milestoneName)
            group.addLayer(self.waterpointLayer)
            group.addLayer(self.boundaryLayer)
            group.addLayer(self.pipelineLayer)
            group.addLayer(self.fenceLayer)
            group.addLayer(self.paddockLayer)

    def setVisible(self, visible):
        """Set the visibility of this milestone's layers."""
        group = self.findGroup()
        if group is not None:
            group.setItemVisibilityChecked(visible)
            group.setExpanded(visible)

    def removeFromMap(self):
        """Remove this milestone from the current map view."""
        group = self.findGroup()
        if group is not None:
            QgsProject.instance().layerTreeRoot().removeChildNode(group)

    def copyTo(self, otherMilestone):
        """Copy all features in this milestone to the target milestone."""
        self.boundaryLayer.copyTo(otherMilestone.boundaryLayer)
        self.waterpointLayer.copyTo(otherMilestone.waterpointLayer)
        self.pipelineLayer.copyTo(otherMilestone.pipelineLayer)
        self.fenceLayer.copyTo(otherMilestone.fenceLayer)
        self.paddockLayer.copyTo(otherMilestone.paddockLayer)

    def deleteFromGeoPackage(self):
        """Delete this milestone from the GeoPackage file."""
        if not self.isLoaded:
            raise PaddockPowerError(
                "Milestone.deleteFromGeoPackage: cannot delete a milestone that is not loaded")

        def deleteLayerFromGeoPackage(layer):
            gpkgUrl = f"{self.gpkgFile}|layername={layer.name()}"

            processing.run("native:spatialiteexecutesql", {
                'DATABASE': gpkgUrl,
                'SQL': 'drop table {0}'.format(layer.name())
            })

        deleteLayerFromGeoPackage(self.boundaryLayer)
        deleteLayerFromGeoPackage(self.waterpointLayer)
        deleteLayerFromGeoPackage(self.pipelineLayer)
        deleteLayerFromGeoPackage(self.fenceLayer)
        deleteLayerFromGeoPackage(self.paddockLayer)

    def setTool(self, tool):
        """Set the current tool for this milestone."""
        if not isinstance(tool, PaddockPowerMapTool):
            raise PaddockPowerError(
                "Milestone.setTool: tool must be a MilestoneMapTool")

        self.unsetTool()
        self.currentTool = tool
        iface.mapCanvas().setMapTool(self.currentTool)

    def unsetTool(self):
        if self.currentTool is not None:
            self.currentTool.clear()
            self.currentTool.dispose()
            iface.mapCanvas().unsetMapTool(self.currentTool)
            self.currentTool = None

    def setSelectedFence(self, fence):
        if fence is not None and not isinstance(fence, Fence):
            raise PaddockPowerError(
                "Milestone.setSelectedFence: fence must be a Fence")
        self.selectedFence = fence
        self.selectedFenceChanged.emit(self.selectedFence)

    def setSelectedPaddock(self, paddock):
        if paddock is not None and not isinstance(paddock, Paddock):
            raise PaddockPowerError(
                "Milestone.setSelectedPaddock: paddock must be a Paddock")
        self.selectedPaddock = paddock
        self.selectedPaddockChanged.emit(self.selectedPaddock)

    def setSelectedPipeline(self, pipeline):
        if pipeline is not None and not isinstance(pipeline, Pipeline):
            raise PaddockPowerError(
                "Milestone.setSelectedPipeline: pipeline must be a Pipeline")
        self.selectedPipeline = pipeline
        self.selectedPipelineChanged.emit(self.selectedPipeline)

    def draftFence(self, fence):
        if not isinstance(fence, Fence):
            raise PaddockPowerError(
                "Milestone.draftFence: fence must be a Fence")

        normalisedFenceLine, supersededPaddocks = self.paddockLayer.getCrossedPaddocks(
            fence.geometry())

        if normalisedFenceLine is None or normalisedFenceLine.isEmpty() or not supersededPaddocks:
            guiError(
                "The Fence you have sketched does not cross or touch any Paddocks.")
            return

        fence.setGeometry(normalisedFenceLine)
        fence.setFenceBuildOrder(self.fenceLayer.nextBuildOrder())
        fence.setStatus(FeatureStatus.Draft)
        fence.recalculate()

        self.fenceLayer.instantAddFeature(fence)
        draftFence = self.fenceLayer.getFenceByBuildOrder(
            fence.fenceBuildOrder())
        return draftFence

    def planFence(self, fence):
        """Return a tuple consisting of a normalised fence geometry, a list of superseded paddocks 'fully crossed' by the cropped fence geometry,
           and a list of planned paddocks resulting from splitting the paddocks using the cropped fence geometry."""

        if not isinstance(fence, Fence):
            raise PaddockPowerError(
                "Milestone.planFence: fence must be a Fence")

        try:
            self.paddockLayer.startEditing()
            self.fenceLayer.startEditing()

            supersededPaddocks, plannedPaddocks = self.paddockLayer.planPaddocks(
                fence)

            fence.setSupersededPaddocks(supersededPaddocks)
            fence.setPlannedPaddocks(plannedPaddocks)
            fence.setStatus(FeatureStatus.Planned)
            fence.recalculate()
            self.fenceLayer.updateFeature(fence)

            self.fenceLayer.commitChanges()
            self.paddockLayer.commitChanges()
        except Exception as e:
            self.fenceLayer.rollBack()
            self.paddockLayer.rollBack()
            raise PaddockPowerError(
                f"Milestone.planFence: failed to plan fence {str(e)}")

        return self.fenceLayer.getFenceByBuildOrder(fence.fenceBuildOrder())

    def undoPlanFence(self, fence):
        """Undo the Paddock changes created by a planned Fence and return the Fence to Draft status."""
        if not isinstance(fence, Fence):
            raise PaddockPowerError(
                "Milestone.undoFence: fence must be a Fence")

        # if fence.fenceBuildOrder() < self.fenceLayer.currentBuildOrder():
        #     guiError("You can only undo the most recently planned Fence.")
        #     return

        try:
            self.paddockLayer.startEditing()
            self.fenceLayer.startEditing()

            self.paddockLayer.undoPlanPaddocks(fence)
            fence.setStatus(FeatureStatus.Draft)
            # fence.setSupersededPaddocks([])
            fence.setPlannedPaddocks([])
            self.fenceLayer.instantUpdateFeature(fence)

            self.fenceLayer.commitChanges
            self.paddockLayer.commitChanges()
        except Exception as e:
            self.fenceLayer.rollBack()
            self.paddockLayer.rollBack()
            raise PaddockPowerError(
                f"Milestone.undoPlanFence: failed to undo fence {str(e)}")

        return self.fenceLayer.getFenceByBuildOrder(fence.fenceBuildOrder())

    def disconnectAll(self):
        """Disconnect all signals from the milestone."""
        self.selectedFenceChanged.disconnect()
        self.selectedPaddockChanged.disconnect()
        self.selectedPipelineChanged.disconnect()
        self.milestoneDataChanged.disconnect()
