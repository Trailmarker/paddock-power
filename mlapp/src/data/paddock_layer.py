# -*- coding: utf-8 -*-
from qgis.core import QgsField, QgsWkbTypes
from qgis.PyQt.QtCore import QVariant

from .paddock_power_vector_layer import (PaddockPowerVectorLayer,
                                         PaddockPowerVectorLayerSourceType,
                                         PaddockPowerVectorLayerType)


class PaddockLayer(PaddockPowerVectorLayer):

    SCHEMA = [
        QgsField(name="Paddock Name", type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Paddock Area (km²)", type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Paddock Perimeter (km)", type=QVariant.Double,
                 typeName="Real", len=0, prec=0, comment="", subType=QVariant.Invalid),
    ]

    STYLE = "paddock"

    TYPE = PaddockPowerVectorLayerType.Paddock

    def __init__(self, sourceType=PaddockPowerVectorLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Paddock layer."""

        super(PaddockLayer, self).__init__(sourceType,
                                           layerName,
                                           QgsWkbTypes.MultiPolygon,
                                           self.SCHEMA,
                                           gpkgFile,
                                           styleName=self.STYLE)
