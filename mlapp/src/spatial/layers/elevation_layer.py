# -*- coding: utf-8 -*-

from qgis.core import QgsProject, QgsRasterLayer

from ...models.glitch import Glitch
from ...utils import qgsDebug


def rasterGpkgUrl(gpkgFile, layerName):
    """Return a URL for a raster layer in a GeoPackage file."""
    # different from QgsVectorLayer GeoPackage URL format!
    return f"GPKG:{gpkgFile}:{layerName}"


class ElevationLayer(QgsRasterLayer):

    @classmethod
    def detectAndRemove(cls, gpkgFile, layerName):
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
