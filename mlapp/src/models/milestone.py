# -*- coding: utf-8 -*-
from os import path

import processing

from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.core import QgsProject
from qgis.utils import iface

from ..spatial.features.fence import Fence
from ..spatial.features.paddock import Paddock
from ..spatial.features.pipeline import Pipeline
from ..spatial.layers.boundary_layer import BoundaryLayer
from ..spatial.layers.fence_layer import FenceLayer
from ..spatial.layers.paddock_layer import PaddockLayer
from ..spatial.layers.feature_layer import FeatureLayerSourceType
from ..spatial.layers.pipeline_layer import PipelineLayer
from ..spatial.layers.waterpoint_layer import WaterpointLayer

from ..widgets.paddock_power_map_tool import PaddockPowerMapTool

from .glitch import Glitch


class Milestone(QObject):
    # emit this signal when paddocks are updated
    selectedFenceChanged = pyqtSignal(Fence)
    selectedPaddockChanged = pyqtSignal(Paddock)
    selectedPipelineChanged = pyqtSignal(Pipeline)
    milestoneDataChanged = pyqtSignal()

    def __init__(self, milestoneName, gpkgFile, elevationLayer):
        super().__init__()

        self.milestoneName = milestoneName
        self.gpkgFile = gpkgFile
        self.elevationLayer = elevationLayer

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
        waterpoint = WaterpointLayer(self.elevationLayer,
            layerName=f"{self.milestoneName} Waterpoints")
        pipeline = PipelineLayer(self.elevationLayer, layerName=f"{self.milestoneName} Pipeline")
        paddock = PaddockLayer(layerName=f"{self.milestoneName} Paddocks")
        fence = FenceLayer(paddock, self.elevationLayer, layerName=f"{self.milestoneName} Fence")

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
        self.boundaryLayer = BoundaryLayer(sourceType=FeatureLayerSourceType.File,
                                           layerName=boundaryLayerName, gpkgFile=self.gpkgFile)
        waterpointLayerName = f"{self.milestoneName} Waterpoints"
        self.waterpointLayer = WaterpointLayer(self.elevationLayer,
                                               sourceType=FeatureLayerSourceType.File,
                                               layerName=waterpointLayerName, gpkgFile=self.gpkgFile)
        pipelineLayerName = f"{self.milestoneName} Pipeline"
        self.pipelineLayer = PipelineLayer(self.elevationLayer,
                                           sourceType=FeatureLayerSourceType.File,
                                           layerName=pipelineLayerName, gpkgFile=self.gpkgFile)
        paddockLayerName = f"{self.milestoneName} Paddocks"
        self.paddockLayer = PaddockLayer(sourceType=FeatureLayerSourceType.File,
                                         layerName=paddockLayerName, gpkgFile=self.gpkgFile)
        fenceLayerName = f"{self.milestoneName} Fence"
        self.fenceLayer = FenceLayer(self.paddockLayer,
                                     self.elevationLayer,
                                     sourceType=FeatureLayerSourceType.File,
                                     layerName=fenceLayerName, gpkgFile=self.gpkgFile)

        self.connectLayerDataEvents()

        self.isLoaded = True

    def connectLayerDataEvents(self):
        """Connect to layer data changed events."""
        # TODO self.boundaryLayer, self.waterpointLayer, 
        for layer in [self.pipelineLayer, self.fenceLayer, self.paddockLayer]:
            layer.afterCommitChanges.connect(self.milestoneDataChanged)

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
            raise Glitch(
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
            raise Glitch(
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
            raise Glitch(
                "Milestone.setSelectedFence: fence must be a Fence")
        self.selectedFence = fence
        self.selectedFenceChanged.emit(self.selectedFence)

    def setSelectedPaddock(self, paddock):
        if paddock is not None and not isinstance(paddock, Paddock):
            raise Glitch(
                "Milestone.setSelectedPaddock: paddock must be a Paddock")
        self.selectedPaddock = paddock
        self.selectedPaddockChanged.emit(self.selectedPaddock)

    def setSelectedPipeline(self, pipeline):
        if pipeline is not None and not isinstance(pipeline, Pipeline):
            raise Glitch(
                "Milestone.setSelectedPipeline: pipeline must be a Pipeline")
        self.selectedPipeline = pipeline
        self.selectedPipelineChanged.emit(self.selectedPipeline)

    def planFence(self, fence):
        """Return a tuple consisting of a normalised fence geometry, a list of superseded paddocks 'fully crossed' by the cropped fence geometry,
           and a list of planned paddocks resulting from splitting the paddocks using the cropped fence geometry."""

        # Start editing all the related layers ...

        fence.plan.emit()
        #fence.upsert()
        #return self.fenceLayer.getFenceByBuildOrder(fence.buildOrder)

    def undoPlanFence(self, fence):
        """Undo the Paddock changes created by a planned Fence and return the Fence to Draft status."""
        if not isinstance(fence, Fence):
            raise Glitch(
                "Milestone.undoFence: fence must be a Fence")

        fence.undoPlanFence()

        return self.fenceLayer.getFenceByBuildOrder(fence.buildOrder)

    def disconnectAll(self):
        """Disconnect all signals from the milestone."""
        self.selectedFenceChanged.disconnect()
        self.selectedPaddockChanged.disconnect()
        self.selectedPipelineChanged.disconnect()
        self.milestoneDataChanged.disconnect()
