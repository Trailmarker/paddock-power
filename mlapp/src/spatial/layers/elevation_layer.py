# -*- coding: utf-8 -*-
from os import path
import sqlite3

from qgis.core import QgsProject, QgsRasterLayer

from ...models.glitch import Glitch
from ...utils import PLUGIN_NAME


def rasterGpkgUrl(gpkgFile, layerName):
    """Return a URL for a raster layer in a GeoPackage file."""
    # different from QgsVectorLayer GeoPackage URL format!
    return f"GPKG:{gpkgFile}:{layerName}"


class ElevationLayer(QgsRasterLayer):

    @classmethod
    def detectInGeoPackage(_, gpkgFile):
        """Find an elevation layer in a project GeoPackage."""
        try:
            if not path.exists(gpkgFile):
                return None
            
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
                    f"{PLUGIN_NAME} found multiple possible elevation layers in {gpkgFile}")
        except BaseException:
            return None

    def detectAndRemove(self, gpkgFile, layerName):
        """Detect if a layer is already in the map, and if so, return it."""
        rasterUrl = rasterGpkgUrl(gpkgFile, layerName)

        layers = [l for l in QgsProject.instance().mapLayers().values()]
        for layer in layers:
            if layer.source() == rasterUrl:
                QgsProject.instance().removeMapLayer(layer.id())

    def __init__(self, gpkgFile, layerName):
        """Create a new elevation layer."""

        assert(gpkgFile is not None)
        assert(layerName is not None)

        # Note ths URL format is different from QgsVectorLayer!
        rasterUrl = rasterGpkgUrl(gpkgFile, layerName)
        super().__init__(rasterUrl, baseName=layerName)

        self.detectAndRemove(gpkgFile, layerName)

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
