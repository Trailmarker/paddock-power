# -*- coding: utf-8 -*-
from os import path

import processing

from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.core import QgsProject
from qgis.utils import iface

from ..layer.paddock_power_vector_layer import PaddockPowerLayerSourceType
from ..layer.boundary_layer import BoundaryLayer
from ..layer.waterpoint_layer import WaterpointLayer
from ..layer.pipeline_layer import PipelineLayer
from ..layer.fence_layer import FenceLayer
from ..layer.paddock_layer import PaddockLayer

from ..tools.paddock_power_map_tool import PaddockPowerMapTool

from .paddock_power_error import PaddockPowerError


class Milestone(QObject):
    # emit this signal when paddocks are updated
    paddocksUpdated = pyqtSignal()

    def __init__(self, milestoneName, gpkgFile):
        super(Milestone, self).__init__()

        self.milestoneName = milestoneName
        self.gpkgFile = gpkgFile
        self.currentTool = None
        self.isLoaded = False

    def create(self):
        """Create this milestone in its GeoPackage."""
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

    def planFence(self):
        """Plan a fence for this milestone."""
        self.fenceLayer.startEditing()
        