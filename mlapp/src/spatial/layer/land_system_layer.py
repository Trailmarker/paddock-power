# -*- coding: utf-8 -*-
from qgis.core import QgsWkbTypes

from ..feature.land_system import LandSystem, asLandSystem
from .paddock_power_vector_layer import PaddockPowerVectorLayer, PaddockPowerLayerSourceType


class LandSystemLayer(PaddockPowerVectorLayer):

    STYLE = "land_system"

    def __init__(self, sourceType=PaddockPowerLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Pipeline layer."""

        super(LandSystemLayer, self).__init__(sourceType,
                                               layerName,
                                               QgsWkbTypes.LineString,
                                               LandSystem.SCHEMA,
                                               gpkgFile,
                                               styleName=self.STYLE)

        # Convert all QGIS features to Fences
        self.setFeatureAdapter(asLandSystem)

