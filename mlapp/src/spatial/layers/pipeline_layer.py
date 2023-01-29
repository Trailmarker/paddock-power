# -*- coding: utf-8 -*-
from ..features.pipeline import Pipeline
from ..fields.schemas import PipelineSchema
from .imported_feature_layer import ImportedFeatureLayer


class PipelineLayer(ImportedFeatureLayer):

    NAME = "Pipelines"
    STYLE = "pipeline"

    def __init__(self,
                 workspaceFile):
        """Create or open a Pipeline layer."""

        super().__init__(Pipeline,
                         workspaceFile,
                         layerName=PipelineLayer.NAME,
                         styleName=PipelineLayer.STYLE)
        
    def getSchema(self):
        """Return the Schema for this layer."""
        return PipelineSchema
        
    
    def getWkbType(self):
        """Return the WKB type for this layer."""
        return PipelineSchema.wkbType

  
