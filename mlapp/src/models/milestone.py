# -*- coding: utf-8 -*-
from os import path
from mlapp.src.spatial.layers.waterpoint_buffer_layer import WaterpointBufferLayer

import processing

from qgis.PyQt.QtCore import QObject, pyqtSignal, pyqtSlot
from qgis.core import QgsProject
from qgis.utils import iface

from ..spatial.features.feature import Feature
from ..spatial.features.fence import Fence
from ..spatial.features.paddock import Paddock
from ..spatial.features.pipeline import Pipeline
from ..spatial.layers.boundary_layer import BoundaryLayer
from ..spatial.layers.fence_layer import FenceLayer
from ..spatial.layers.paddock_layer import PaddockLayer
from ..spatial.layers.pipeline_layer import PipelineLayer
from ..spatial.layers.waterpoint_layer import WaterpointLayer

from ..utils import qgsDebug

from ..widgets.paddock_power_map_tool import PaddockPowerMapTool

from .glitch import Glitch


class Milestone(QObject):
    # emit this signal when a selected Feature is updated
    selectedFeatureChanged = pyqtSignal(Feature)
    milestoneDataChanged = pyqtSignal()

    def __init__(self, milestoneName, gpkgFile, elevationLayer):
        super().__init__()

        self.milestoneName = milestoneName
        self.gpkgFile = gpkgFile
        self.elevationLayer = elevationLayer

        boundaryLayerName = f"{self.milestoneName} Boundary"
        self.boundaryLayer = BoundaryLayer(gpkgFile, boundaryLayerName)
        waterpointBufferLayerName = f"{self.milestoneName} Waterpoint Buffers"
        self.waterpointBufferLayer = WaterpointBufferLayer(gpkgFile, waterpointBufferLayerName)
        waterpointLayerName = f"{self.milestoneName} Waterpoints"
        self.waterpointLayer = WaterpointLayer(gpkgFile, waterpointLayerName,
                                               waterpointBufferLayer=self.waterpointBufferLayer,
                                               elevationLayer=self.elevationLayer)
        pipelineLayerName = f"{self.milestoneName} Pipeline"
        self.pipelineLayer = PipelineLayer(gpkgFile, pipelineLayerName,
                                           elevationLayer=self.elevationLayer)
        paddockLayerName = f"{self.milestoneName} Paddocks"
        self.paddockLayer = PaddockLayer(gpkgFile, paddockLayerName)
        fenceLayerName = f"{self.milestoneName} Fence"
        self.fenceLayer = FenceLayer(gpkgFile, fenceLayerName,
                                     paddockLayer=self.paddockLayer,
                                     elevationLayer=self.elevationLayer)
        
        self.currentTool = None
        self.isLoaded = False

        self.selectedFeatures = {
            Fence: None,
            Paddock: None,
            Pipeline: None
        }

        self.connectLayerDataEvents()

    @property
    def selectedFence(self):
        """Get the currently selected fence."""
        return self.selectedFeatures[Fence]

    @property
    def selectedPaddock(self):
        """Get the currently selected paddock."""
        return self.selectedFeatures[Paddock]

    @property
    def selectedPipeline(self):
        """Get the currently selected pipeline."""
        return self.selectedFeatures[Pipeline]

    def connectLayerDataEvents(self):
        """Connect to layer data changed events."""
        # TODO self.boundaryLayer, self.waterpointLayer, 
        for layer in [self.pipelineLayer, self.fenceLayer, self.paddockLayer]:
            layer.selectionChanged.connect(lambda selection, *_: self.onLayerSelectionChanged(layer, selection))
            layer.afterCommitChanges.connect(lambda: self.milestoneDataChanged.emit)

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

    def setSelectedFeature(self, feature):
        if feature is not None and not isinstance(feature, Feature):
            raise Glitch(
                "You can't select an object that is not a Feature")
        self.selectedFeatures[type(feature)] = feature
        self.selectedFeatureChanged.emit(feature)

    @pyqtSlot()
    def onLayerSelectionChanged(self, layer, selection):
        if len(selection) == 1:
            feature = layer.getFeatureById(selection[0])
            qgsDebug(f"onLayerSelectionChanged: {feature or 'None'}")
            if feature is not None:
                self.setSelectedFeature(feature)

    def disconnectAll(self):
        """Disconnect all signals from the milestone."""
        self.selectedFeatureChanged.disconnect()
        self.milestoneDataChanged.disconnect()
