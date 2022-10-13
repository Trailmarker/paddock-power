# -*- coding: utf-8 -*-
from qgis.core import QgsWkbTypes

from ..feature.pipeline import Pipeline
from .paddock_power_vector_layer import PaddockPowerVectorLayer, PaddockPowerLayerSourceType


class PipelineLayer(PaddockPowerVectorLayer):

    STYLE = "pipeline"

    def __init__(self, sourceType=PaddockPowerLayerSourceType.Memory, layerName=None, gpkgFile=None):
        """Create or open a Pipeline layer."""

        super(PipelineLayer, self).__init__(sourceType,
                                            layerName,
                                            QgsWkbTypes.LineString,
                                            Pipeline.SCHEMA,
                                            gpkgFile,
                                            styleName=self.STYLE)

