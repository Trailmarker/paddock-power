# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsField, QgsWkbTypes

from .paddock_power_vector_layer import PaddockPowerVectorLayer, PaddockPowerVectorLayerSourceType, PaddockPowerVectorLayerType


class LandSystemsLayer(PaddockPowerVectorLayer):

    SCHEMA = [
        QgsField(name="Land System", type=QVariant.String, typeName="String",
                 len=50, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Map Unit", type=QVariant.String, typeName="String",
                 len=10, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Original Land System", type=QVariant.String,
                 typeName="String", len=50, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Original Map Unit", type=QVariant.String, typeName="String",
                 len=10, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Landscape Class", type=QVariant.String, typeName="String",
                 len=50, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Class Description", type=QVariant.String, typeName="String",
                 len=254, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Erosion Risk", type=QVariant.String, typeName="String",
                 len=100, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Land Unit/Land System Area (km²)", type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="AE/km²", type=QVariant.Double, typeName="Real",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
    ]

    # TODO - add a style for this layer type
    STYLE = None

    def __init__(self, sourceType=PaddockPowerVectorLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Pipeline layer."""

        super(LandSystemsLayer, self).__init__(sourceType,
                                               layerName,
                                               QgsWkbTypes.LineString,
                                               self.SCHEMA,
                                               gpkgFile,
                                               styleName=self.STYLE)

    def getLayerType(self):
        """Return the Paddock Power layer type."""
        return PaddockPowerVectorLayerType.LandSystems
