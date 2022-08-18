# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsField, QgsWkbTypes

from .paddock_power_vector_layer import PaddockPowerVectorLayer, PaddockPowerVectorLayerSourceType, PaddockPowerVectorLayerType


class PipelineLayer(PaddockPowerVectorLayer):

    SCHEMA = [
        QgsField(name="Name", type=QVariant.String, typeName="String",
                 len=0, prec=0, comment="", subType=QVariant.Invalid),
        QgsField(name="Length (km)", type=QVariant.Double, typeName="Real",
                 len=0, prec=0, comment="", subType=QVariant.Invalid)
    ]
    STYLE = "pipeline"

    TYPE = PaddockPowerVectorLayerType.Pipeline

    def __init__(self, sourceType=PaddockPowerVectorLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Pipeline layer."""

        super(PipelineLayer, self).__init__(sourceType,
                                            layerName,
                                            QgsWkbTypes.LineString,
                                            self.SCHEMA,
                                            gpkgFile,
                                            styleName=self.STYLE)
