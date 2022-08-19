# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsField, QgsWkbTypes

from .paddock_power_vector_layer import PaddockPowerVectorLayer, PaddockPowerVectorLayerSourceType, PaddockPowerVectorLayerType


class FenceLayer(PaddockPowerVectorLayer):

    SCHEMA = [
        QgsField(name="Length (km)", type=QVariant.Double, typeName="Real",
                 len=0, prec=0, comment="", subType=QVariant.Invalid)
    ]

    STYLE = "fence"

    def __init__(self, sourceType=PaddockPowerVectorLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Fence layer."""

        super(FenceLayer, self).__init__(sourceType,
                                         layerName,
                                         QgsWkbTypes.LineString,
                                         self.SCHEMA,
                                         gpkgFile,
                                         styleName=self.STYLE)

    def getLayerType(self):
        """Return the Paddock Power layer type."""
        return PaddockPowerVectorLayerType.Fence
