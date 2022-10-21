# -*- coding: utf-8 -*-

from qgis.core import QgsProject, QgsRasterLayer

from ...utils import qgsDebug


def rasterGpkgUrl(gpkgFile, layerName):
    """Return a URL for a raster layer in a GeoPackage file."""
    # different from QgsVectorLayer GeoPackage URL format!
    return f"GPKG:{gpkgFile}:{layerName}"


class ElevationLayer(QgsRasterLayer):

    def __new__(cls, *args, **kwargs):

        gpkgFile = kwargs.get('gpkgFile', None)
        layerName = kwargs.get('layerName', None)

        # different from QgsVectorLayer GeoPackage URL format!
        rasterUrl = rasterGpkgUrl(gpkgFile, layerName)

        for layer in QgsProject.instance().mapLayers().values():
            if layer.source() == rasterUrl:
                qgsDebug(f"{cls.__name__}.__new__: Coercing existing QgsRasterLayer {layer.name()}")
                QgsProject.instance().removeMapLayer(layer.id())
                layer.setName(layerName)
                layer.__class__ = cls
                return layer

        return super().__new__(cls)

    def __init__(self, layerName=None, gpkgFile=None):
        """Create a new elevation layer."""

        assert(layerName is not None)
        assert(gpkgFile is not None)

        rasterUrl = rasterGpkgUrl(gpkgFile, layerName)
        super().__init__(rasterUrl, baseName=layerName)

    def addToMap(self, group):
        """Ensure the layer is in the map in the target group, adding it if necessary."""

        if group is None:
            group = QgsProject.instance().layerTreeRoot()

        if self.source() not in [layer.source() for layer in QgsProject.instance().mapLayers().values()]:
            group.addLayer(self)
            QgsProject.instance().addMapLayer(self, False)
