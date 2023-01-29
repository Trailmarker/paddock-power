# -*- coding: utf-8 -*-
from functools import cached_property
from os import path
import sqlite3

from qgis.PyQt.QtCore import pyqtSlot

from qgis.core import QgsProject, QgsRasterLayer

from ...models.glitch import Glitch
from ...utils import PLUGIN_NAME, qgsError, resolveStylePath
from ..fields.timeframe import Timeframe

class ElevationLayer(QgsRasterLayer):

    NAME = "Elevation Mapping"
    STYLE = "elevation"

    @classmethod
    def detectAndRemoveAllOfType(cls):
        """Detect if any layers of the same type are already in the map, and if so, remove them. Use with care."""
        layers = [l for l in QgsProject.instance().mapLayers().values() if type(l).__name__ == cls.__name__]
        for layer in layers:
            QgsProject.instance().removeMapLayer(layer.id())

    @staticmethod
    def _rasterGpkgUrl(workspaceFile, layerName):
        """Return a URL for a raster layer in a GeoPackage file."""
        # different from QgsVectorLayer GeoPackage URL format!
        return f"GPKG:{workspaceFile}:{layerName}"


    @classmethod
    def detectInGeoPackage(_, workspaceFile):
        """Find an elevation layer in a workspace GeoPackage."""
        try:
            if not path.exists(workspaceFile):
                return None

            db = sqlite3.connect(workspaceFile)
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
                    f"{PLUGIN_NAME} found multiple possible elevation layers in {workspaceFile}")
        except BaseException:
            return None


    def __init__(self, workspaceFile, layerName=None, *args, **kwargs):
        """Create a new elevation layer."""

        self._workspace = None
        
        # Route changes to this layer *through* the Paddock Power
        # workspace so other objects can respond
        self._blockWorkspaceConnnection = False

        layerName = layerName or ElevationLayer.NAME
        
        styleName = kwargs.pop("styleName", ElevationLayer.STYLE)

        # Note ths URL format is different from QgsVectorLayer!
        rasterUrl = ElevationLayer._rasterGpkgUrl(workspaceFile, layerName)
        super().__init__(rasterUrl, baseName=layerName)
        
        self.applyNamedStyle(styleName)
        
        self.addInBackground()

    @cached_property
    def typeName(self):
        """Return the FeatureLayer's type name."""
        return type(self).__name__
    
    
    def __repr__(self):
        """Return a string representation of the Field."""
        return f"{self.typeName}(name={self.name()})"


    def __str__(self):
        """Convert the Field to a string representation."""
        return repr(self)
   
    # Workspace interface 
    @property
    def connectedToWorkspace(self):
        """Are we both connected to the workspace and not temporarily blocked."""
        return self._workspace and not self._blockWorkspaceConnnection

    @property
    def workspace(self):
        f"""The {PLUGIN_NAME} workspace we are connected to."""
        return self._workspace

    @property
    def currentTimeframe(self):
        """Get the current timeframe for this layer (same as that of the workspace)."""
        return self.workspace.currentTimeframe if self.connectedToWorkspace else Timeframe.Undefined


    def connectWorkspace(self, workspace):
        """Hook it up to uor veins."""
        self._workspace = workspace
        self.workspaceConnectionChanged.emit()


    def workspaceLayer(self, layerType):
        """Get a layer we depend on to work with by type."""
        if self.connectedToWorkspace:
            return self.workspace.workspaceLayers.getLayer(layerType)
        else:
            qgsError(f"{self.typeName}.depend({layerType}): no workspace connection")
    
    
    def findGroup(self, name=None):
        """Find the group for this layer in the map."""
        return QgsProject.instance().layerTreeRoot().findGroup(name) if name else None

    
    def addInBackground(self):
        """Add this layer to the map in the background."""
        QgsProject.instance().addMapLayer(self, False)
        
        
    def addToMap(self, group=None):
        """Ensure the layer is in the map in the target group, adding it if necessary."""
        group = group or self.findGroup() or QgsProject.instance().layerTreeRoot()
        group.addLayer(self)
        
    
    def removeFromMap(self, group):
        """Remove the layer from the map in the target group, if it is there."""
        group = group or self.findGroup() or QgsProject.instance().layerTreeRoot()
        node = group.findLayer(self.id())
        if node:
            group.removeChildNode(node)
    
    
    def setVisible(self, group, visible):
        """Set the layer's visibility."""
        group = group or self.findGroup() or QgsProject.instance().layerTreeRoot()
        node = group.findLayer(self.id())
        if node:
            node.setItemVisibilityChecked(visible)

    
    def applyNamedStyle(self, styleName):
        """Apply a style to the layer."""
        # Optionally apply a style to the layer
        if styleName:
            stylePath = resolveStylePath(styleName)
            self.loadNamedStyle(stylePath)
        self.triggerRepaint()
    
    @pyqtSlot(Timeframe)  
    def onCurrentTimeframeChanged(self, timeframe):
        """Handle the current timeframe changing."""
        pass
        
    @pyqtSlot()   
    def onWorkspaceConnectionChanged(self):
        """Handle the workspace connection changing."""
        pass
