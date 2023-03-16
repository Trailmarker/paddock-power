# -*- coding: utf-8 -*-
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
