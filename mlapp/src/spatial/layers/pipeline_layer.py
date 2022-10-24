# -*- coding: utf-8 -*-
from ..features.pipeline import Pipeline
from .elevation_layer import ElevationLayer
from .feature_layer import FeatureLayer


class PipelineLayer(FeatureLayer):

    STYLE = "pipeline"

    @classmethod
    def getFeatureType(cls):
        return Pipeline

    def __init__(self, gpkgFile, layerName, elevationLayer: ElevationLayer):
        """Create or open a Pipeline layer."""

        super().__init__(gpkgFile,
                         layerName,
                         styleName=PipelineLayer.STYLE)

        self.elevationLayer = elevationLayer

    def wrapFeature(self, feature):
        return self.getFeatureType()(self, self.elevationLayer, feature)
