# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsField, QgsWkbTypes

from .paddock_power_vector_layer import PaddockPowerVectorLayer, PaddockPowerLayerSourceType, PaddockPowerVectorLayerType


class BoundaryLayer(PaddockPowerVectorLayer):

    SCHEMA = [
        QgsField(name="Property Name", type=QVariant.String, typeName="String",
                 len=50, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Property Area (km²)", type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid)
    ]

    STYLE = "boundary"

    def __init__(self, sourceType=PaddockPowerLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Boundary layer."""

        super(BoundaryLayer, self).__init__(sourceType,
                                            layerName,
                                            QgsWkbTypes.MultiPolygon,
                                            self.SCHEMA,
                                            gpkgFile,
                                            styleName=self.STYLE)

    def getLayerType(self):
        """Return the Paddock Power layer type."""
        return PaddockPowerVectorLayerType.Boundary
