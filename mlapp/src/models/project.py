# -*- coding: utf-8 -*-
import sqlite3
from mlapp.src.widgets.paddock_power_map_tool import PaddockPowerMapTool

from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot, QObject
from qgis.core import QgsProject
from qgis.utils import iface

# -*- coding: utf-8 -*-
from ..spatial.features.boundary import Boundary
from ..spatial.features.waterpoint import Waterpoint
from ..spatial.features.pipeline import Pipeline
from ..spatial.features.feature import Feature
from ..spatial.features.fence import Fence
from ..spatial.features.paddock import Paddock
from ..spatial.features.land_system import LandSystem
from ..spatial.layers.elevation_layer import ElevationLayer
from ..spatial.layers.boundary_layer import BoundaryLayer
from ..spatial.layers.fence_layer import FenceLayer
from ..spatial.layers.paddock_layer import PaddockLayer
from ..spatial.layers.pipeline_layer import PipelineLayer
from ..spatial.layers.waterpoint_buffer_layer import WaterpointBufferLayer
from ..spatial.layers.waterpoint_layer import WaterpointLayer
from ..utils import qgsDebug, resolveGeoPackageFile
from .glitch import Glitch


class Project(QObject):
    PROJECT_BASE_DATA_GROUP = "Base Data"

    PADDOCK_POWER_FEATURE_TYPES = (
        Boundary, Waterpoint, Pipeline, Fence, Paddock, LandSystem)

    # emit this signal when a selected Feature is updated
    selectedFeatureChanged = pyqtSignal(Feature)
    projectDataChanged = pyqtSignal()

    def __init__(self, gpkgFile=None, projectName=None):
        super().__init__()

        gpkgFile = gpkgFile or resolveGeoPackageFile()
        self.gpkgFile = gpkgFile
        self.projectName = projectName or "Paddock Power"

        self.elevationLayer = None
        elevationLayerName = self.findElevationLayer(self.gpkgFile)
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

        self.currentTool = None

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
            layer.afterCommitChanges.connect(lambda: self.projectDataChanged.emit)

    def findGroup(self):
        """Find this Project's group in the Layers panel."""
        group = QgsProject.instance().layerTreeRoot().findGroup(self.projectName)
        if group is None:
            group = QgsProject.instance().layerTreeRoot().insertGroup(0, self.projectName)
        return group

    def addToMap(self, group=None):
        """Add this Project to the map."""
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
        self.waterpointLayer.removeFromMap(group)
        self.boundaryLayer.removeFromMap(group)
        self.pipelineLayer.removeFromMap(group)
        self.fenceLayer.removeFromMap(group)
        self.waterpointBufferLayer.removeFromMap(group)
        self.paddockLayer.removeFromMap(group)
        # self.landSystemLayer.removeFromMap(group)
        self.elevationLayer.removeFromMap(group)
        QgsProject.instance().layerTreeRoot().removeChildNode(group)

    def setTool(self, tool):
        """Set the current tool for this Project."""
        if not isinstance(tool, PaddockPowerMapTool):
            raise Glitch(
                "Project.setTool: tool must be a PaddockPowerMapTool")

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

    @classmethod
    def findElevationLayer(cls, gpkgFile):
        """Find the elevation layer in a project GeoPackage."""
        db = sqlite3.connect(gpkgFile)
        cursor = db.cursor()
        cursor.execute(
            "SELECT table_name, data_type FROM gpkg_contents WHERE data_type = '2d-gridded-coverage'")
        grids = cursor.fetchall()

        if len(grids) == 0:
            return None
        elif len(grids) == 1:
            return grids[0][0]
        else:
            raise Glitch(
                f"Project.findElevationLayer: multiple elevation layers found in {gpkgFile}")
