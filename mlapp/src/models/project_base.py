# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QObject

from qgis.core import QgsProject

from ..spatial.layers.elevation_layer import ElevationLayer
from ..spatial.layers.boundary_layer import BoundaryLayer
from ..spatial.layers.fence_layer import FenceLayer
from ..spatial.layers.paddock_layer import PaddockLayer
from ..spatial.layers.pipeline_layer import PipelineLayer
from ..spatial.layers.waterpoint_buffer_layer import WaterpointBufferLayer
from ..spatial.layers.waterpoint_layer import WaterpointLayer
from ..utils import resolveGeoPackageFile


class ProjectBase(QObject):

    def __init__(self, gpkgFile=None, projectName=None):
        super().__init__()

        gpkgFile = gpkgFile or resolveGeoPackageFile()
        self.gpkgFile = gpkgFile
        self.projectName = projectName or "Paddock Power"

        self.elevationLayer = None
        elevationLayerName = ElevationLayer.detectInGeoPackage(self.gpkgFile)
        if elevationLayerName is not None:
            self.elevationLayer = ElevationLayer(self.gpkgFile, elevationLayerName)

        boundaryLayerName = f"Current Boundary"
        self.boundaryLayer = BoundaryLayer(self.gpkgFile, boundaryLayerName)
        waterpointBufferLayerName = f"Current Waterpoint Buffers"
        self.waterpointBufferLayer = WaterpointBufferLayer(self.gpkgFile, waterpointBufferLayerName)
        waterpointLayerName = f"Current Waterpoints"
        self.waterpointLayer = WaterpointLayer(self.gpkgFile, waterpointLayerName,
                                               self.waterpointBufferLayer,
                                               self.elevationLayer)
        pipelineLayerName = f"Current Pipeline"
        self.pipelineLayer = PipelineLayer(self.gpkgFile, pipelineLayerName,
                                           self.elevationLayer)
        paddockLayerName = f"Current Paddocks"
        self.paddockLayer = PaddockLayer(self.gpkgFile, paddockLayerName)
        fenceLayerName = f"Current Fence"
        self.fenceLayer = FenceLayer(self.gpkgFile, fenceLayerName,
                                     self.paddockLayer,
                                     self.elevationLayer)

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
        self.boundaryLayer.addToMap(group)
        self.pipelineLayer.addToMap(group)
        self.fenceLayer.addToMap(group)
        self.waterpointBufferLayer.addToMap(group)
        self.paddockLayer.addToMap(group)
        # self.landSystemLayer.addToMap(group)
        self.elevationLayer.addToMap(group)

    def removeFromMap(self):
        """Remove this Project from the current map view."""
        group = self.findGroup()
        QgsProject.instance().layerTreeRoot().removeChildNode(group)