# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsField, QgsWkbTypes

from .paddock_power_vector_layer import PaddockPowerVectorLayer, PaddockPowerVectorLayerSourceType, PaddockPowerVectorLayerType


class WaterpointLayer(PaddockPowerVectorLayer):

    SCHEMA = [
        QgsField(name="Waterpoint Type", type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint Name", type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint Reference", type=QVariant.String,
                 typeName="String", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint Bore Yield (l/sec)", type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint Bore Report", type=QVariant.String,
                 typeName="String", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint Start Month", type=QVariant.String,
                 typeName="String", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint End Month", type=QVariant.String,
                 typeName="String", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint Longitude", type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint Latitude", type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Waterpoint Elevation", type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid)
    ]

    STYLE = "waterpoint"

    def __init__(self, sourceType=PaddockPowerVectorLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Waterpoint layer."""

        super(WaterpointLayer, self).__init__(sourceType,
                                              layerName,
                                              QgsWkbTypes.Point,
                                              self.SCHEMA,
                                              gpkgFile,
                                              styleName=self.STYLE)

    def getLayerType(self):
        """Return the Paddock Power layer type."""
        return PaddockPowerVectorLayerType.Waterpoint
