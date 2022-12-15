# -*- coding: utf-8 -*-
import os.path
from qgis.PyQt.QtCore import QObject

from qgis.core import QgsProject

from ..spatial.layers.condition_table import ConditionTable
from ..spatial.layers.waterpoint_buffer_layer import WaterpointBufferLayer
from ..spatial.layers.elevation_layer import ElevationLayer
from ..spatial.layers.boundary_layer import BoundaryLayer
from ..spatial.layers.fence_layer import FenceLayer
from ..spatial.layers.land_system_layer import LandSystemLayer
from ..spatial.layers.paddock_layer import PaddockLayer
from ..spatial.layers.pipeline_layer import PipelineLayer
from ..spatial.layers.watered_area_layer import WateredAreaLayer
from ..spatial.layers.waterpoint_layer import WaterpointLayer
from ..utils import PLUGIN_NAME, qgsDebug, resolveGeoPackageFile


class ProjectBase(QObject):

    def __init__(self, gpkgFile=None, projectName=None):
        super().__init__()

        gpkgFile = gpkgFile or resolveGeoPackageFile()
        self.gpkgFile = gpkgFile
        self.projectName = projectName or PLUGIN_NAME

        self.elevationLayer = None
        elevationLayerName = ElevationLayer.detectInGeoPackage(self.gpkgFile)
        if elevationLayerName is not None:
            self.elevationLayer = ElevationLayer(self.gpkgFile, elevationLayerName)

        pipelineLayerName = f"Pipelines"
        self.pipelineLayer = PipelineLayer(self.gpkgFile, pipelineLayerName,
                                           self.elevationLayer)
        
        landSystemLayerName = "Land Systems"
        self.landSystemLayer = LandSystemLayer(self.gpkgFile, landSystemLayerName)
        
        self.conditionTable = ConditionTable(self.gpkgFile, "Condition Table")

        paddockLayerName = f"Paddocks"
        self.paddockLayer = PaddockLayer(
            self.gpkgFile,
            paddockLayerName,
            self.landSystemLayer,
            self.conditionTable)

        waterpointLayerName = f"Waterpoints"
        self.waterpointLayer = WaterpointLayer(self.gpkgFile, waterpointLayerName, self.elevationLayer)

        waterpointBufferLayerName = f"Waterpoint Buffers"
        self.waterpointBufferLayer = WaterpointBufferLayer(self.gpkgFile, waterpointBufferLayerName, self.waterpointLayer, self.paddockLayer)

        # Waterpoints and Waterpoint Buffers are closely linked, not sure how to make this neater
        # Same goes for Paddocks and Watered Areas
        self.waterpointLayer.waterpointBufferLayer = self.waterpointBufferLayer

        wateredAreaLayerName = f"Watered Areas"
        self.wateredAreaLayer = WateredAreaLayer(wateredAreaLayerName, self.paddockLayer, self.waterpointBufferLayer)

        self.paddockLayer.wateredAreaLayer = self.wateredAreaLayer

        fenceLayerName = f"Fences"
        self.fenceLayer = FenceLayer(self.gpkgFile, fenceLayerName,
                                     self.paddockLayer,
                                     self.elevationLayer)

        boundaryLayerName = f"Boundary"
        self.boundaryLayer = BoundaryLayer(boundaryLayerName, self.paddockLayer)

    def findGroup(self):
        """Find this Project's group in the Layers panel."""
        group = QgsProject.instance().layerTreeRoot().findGroup(self.projectName)
        if group is None:
            group = QgsProject.instance().layerTreeRoot().insertGroup(0, self.projectName)
        return group

    def addToMap(self, group=None):
        """Add this Project to the map."""
        self.removeFromMap()

        group = group or self.findGroup()
        self.waterpointLayer.addToMap(group)
        self.pipelineLayer.addToMap(group)
        self.fenceLayer.addToMap(group)
        # Hide Waterpoint Buffers
        self.waterpointBufferLayer.addToMap(group)
        self.wateredAreaLayer.addToMap(group)
        self.landSystemLayer.addToMap(group)
        self.boundaryLayer.addToMap(group)
        self.paddockLayer.addToMap(group)

        if self.elevationLayer is not None:
            self.elevationLayer.addToMap(group)

    def removeFromMap(self):
        """Remove this Project from the current map view."""
        group = self.findGroup()
        QgsProject.instance().layerTreeRoot().removeChildNode(group)
