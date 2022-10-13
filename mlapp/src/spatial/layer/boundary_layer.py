# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsWkbTypes

from ..feature.boundary import Boundary, asBoundary
from .paddock_power_vector_layer import PaddockPowerVectorLayer, PaddockPowerLayerSourceType


class BoundaryLayer(PaddockPowerVectorLayer):

    STYLE = "boundary"

    def __init__(self, sourceType=PaddockPowerLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Boundary layer."""

        super(BoundaryLayer, self).__init__(sourceType,
                                            layerName,
                                            QgsWkbTypes.MultiPolygon,
                                            Boundary.SCHEMA,
                                            gpkgFile,
                                            styleName=self.STYLE)
        # Convert all QGIS features to Boundary objects
        self.setFeatureAdapter(asBoundary)
