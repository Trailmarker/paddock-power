# -*- coding: utf-8 -*-
from ..features.pipeline import Pipeline
from .imported_feature_layer import ImportedFeatureLayer


class PipelineLayer(ImportedFeatureLayer):

    NAME = "Pipelines"
    STYLE = "pipeline"

    @classmethod
    def getFeatureType(cls):
        return Pipeline

    def __init__(self,
                 workspaceFile):
        """Create or open a Pipeline layer."""

        super().__init__(workspaceFile,
                         layerName=PipelineLayer.NAME,
                         styleName=PipelineLayer.STYLE)
