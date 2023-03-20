# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QIcon

from ..utils import PLUGIN_FOLDER
from .features import Pipeline
from .importable_feature_layer import ImportableFeatureLayer


class PipelineLayer(ImportableFeatureLayer):

    LAYER_NAME = "Pipelines"
    STYLE = "pipeline"

    @classmethod
    def getFeatureType(cls):
        return Pipeline

    def __init__(self,
                 workspaceFile,
                 *dependentLayers):
        """Create or open a Pipeline layer."""

        super().__init__(workspaceFile,
                         layerName=PipelineLayer.defaultName(),
                         styleName=PipelineLayer.defaultStyle())
        
    @classmethod    
    def icon(cls):
        """The icon to paint to represent this layer."""
        return QIcon(f":/plugins/{PLUGIN_FOLDER}/images/pipeline.png")
