# -*- coding: utf-8 -*-
from os import path
import sqlite3

from qgis.core import QgsProject, QgsRasterLayer

from ...models.glitch import Glitch
from ...utils import PLUGIN_NAME


def rasterGpkgUrl(workspaceFile, layerName):
    """Return a URL for a raster layer in a GeoPackage file."""
    # different from QgsVectorLayer GeoPackage URL format!
    return f"GPKG:{workspaceFile}:{layerName}"


class ElevationLayer(QgsRasterLayer):

    NAME = "Elevation Mapping"

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

    # def detectAndRemove(self, workspaceFile, layerName):
    #     """Detect if a layer is already in the map, and if so, return it."""
    #     rasterUrl = rasterGpkgUrl(workspaceFile, layerName)

    #     layers = [l for l in QgsProject.instance().mapLayers().values()]
    #     for layer in layers:
    #         if layer.source() == rasterUrl:
    #             QgsProject.instance().removeMapLayer(layer.id())

    def __init__(self, workspaceFile, layerName=None):
        """Create a new elevation layer."""

        assert(workspaceFile is not None)

        layerName = layerName or ElevationLayer.NAME

        # Note ths URL format is different from QgsVectorLayer!
        rasterUrl = rasterGpkgUrl(workspaceFile, layerName)
        super().__init__(rasterUrl, baseName=layerName)

        # self.detectAndRemove(workspaceFile, layerName)

        QgsProject.instance().addMapLayer(self, False)

    def addToMap(self, group):
        """Ensure the layer is in the map in the target group, adding it if necessary."""
        if group is None:
            raise Glitch(
                "ElevationLayer.addToMap: the layer group is not present")
        self.removeFromMap(group)
        group.addLayer(self)

    def removeFromMap(self, group):
        node = group.findLayer(self.id())
        if node:
            group.removeChildNode(node)
