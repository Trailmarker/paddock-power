# -*- coding: utf-8 -*-

from qgis.core import QgsRasterLayer

from .paddock_power_layer_source_type import PaddockPowerLayerSourceType
from ..models.paddock_power_error import PaddockPowerError


class ElevationLayer(QgsRasterLayer):
    def __init__(self, sourceType=PaddockPowerLayerSourceType.Memory, layerName=None,
                 gpkgFile=None):
        """Create a new elevation layer."""

        if sourceType == PaddockPowerLayerSourceType.Memory:
            assert(layerName is not None)

            raise PaddockPowerError(
                "ElevationLayer.__init__: Memory source type not implemented")

        elif sourceType == PaddockPowerLayerSourceType.File:
            assert(layerName is not None)
            assert(gpkgFile is not None)

            # different from QgsVectorLayer GeoPackage URL format!
            rasterGpkgUrl = f"GPKG:{gpkgFile}:{layerName}"

            super(ElevationLayer, self).__init__(
                rasterGpkgUrl, baseName=layerName)

    def addToMap(self, group):
        """Ensure the layer is in the map in the target group, adding it if necessary."""
        if group is None:
            raise PaddockPowerError(
                "PaddockPowerElevationLayer.addToMap: the layer group is not present")

        node = group.findLayer(self.id())
        if node is None:
            group.addLayer(self)
