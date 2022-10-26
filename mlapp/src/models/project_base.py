# -*- coding: utf-8 -*-
from mlapp.src.spatial.layers.watered_area_layer import WateredAreaLayer
from qgis.PyQt.QtCore import QObject

from qgis.core import QgsProject

from ..spatial.layers.condition_table import ConditionTable
from ..spatial.layers.condition_layer import ConditionLayer
from ..spatial.layers.old_condition_record_layer import OldConditionRecordLayer
from ..spatial.layers.elevation_layer import ElevationLayer
from ..spatial.layers.boundary_layer import BoundaryLayer
from ..spatial.layers.fence_layer import FenceLayer
from ..spatial.layers.land_system_layer import LandSystemLayer
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

        waterpointBufferLayerName = f"Waterpoint Buffers"
        self.waterpointBufferLayer = WaterpointBufferLayer(self.gpkgFile, waterpointBufferLayerName)
        waterpointLayerName = f"Waterpoints"
        self.waterpointLayer = WaterpointLayer(self.gpkgFile, waterpointLayerName,
                                               self.waterpointBufferLayer,
                                               self.elevationLayer)
        wateredAreaLayerName = f"Watered Areas"
        self.wateredAreaLayer = WateredAreaLayer(wateredAreaLayerName, self.waterpointBufferLayer)
        pipelineLayerName = f"Pipelines"
        self.pipelineLayer = PipelineLayer(self.gpkgFile, pipelineLayerName,
                                           self.elevationLayer)
        landSystemLayerName = "Land Systems"
        self.landSystemLayer = LandSystemLayer(self.gpkgFile, landSystemLayerName)
        conditionRecordLayerName = f"Paddock Condition"
        self.oldConditionRecordLayer = OldConditionRecordLayer(self.gpkgFile, conditionRecordLayerName)
        paddockLayerName = f"Paddocks"
        self.paddockLayer = PaddockLayer(
            self.gpkgFile,
            paddockLayerName,
            self.landSystemLayer,
            self.waterpointBufferLayer,
            self.oldConditionRecordLayer)
        self.conditionTable = ConditionTable(self.gpkgFile, "Condition Table")
        self.conditionLayer = ConditionLayer(conditionRecordLayerName, self.paddockLayer, self.landSystemLayer, self.waterpointBufferLayer, self.conditionTable)
        fenceLayerName = f"Fences"
        self.fenceLayer = FenceLayer(self.gpkgFile, fenceLayerName,
                                     self.paddockLayer,
                                     self.elevationLayer)
        boundaryLayerName = f"Boundary"
        self.boundaryLayer = BoundaryLayer(boundaryLayerName, self.paddockLayer)

        # qgsDebug("ProjectBase: Layers created")

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
        # self.waterpointBufferLayer.addToMap(group)
        self.wateredAreaLayer.addToMap(group)
        self.boundaryLayer.addToMap(group)
        self.conditionLayer.addToMap(group)
        # Hide Old Condition Records
        # self.oldConditionRecordLayer.addToMap(group)
        self.landSystemLayer.addToMap(group)
        self.landSystemLayer.setVisible(group, False)
        self.paddockLayer.addToMap(group)
        self.elevationLayer.addToMap(group)

    def removeFromMap(self):
        """Remove this Project from the current map view."""
        group = self.findGroup()
        QgsProject.instance().layerTreeRoot().removeChildNode(group)
