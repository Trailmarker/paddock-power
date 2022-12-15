# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ..features.pipeline import Pipeline
from .elevation_layer import ElevationLayer
from .status_feature_layer import StatusFeatureLayer


class PipelineLayer(StatusFeatureLayer):

    STYLE = "pipeline"

    def getFeatureType(self):
        return Pipeline

    def __init__(self, gpkgFile, layerName, elevationLayer: ElevationLayer):
        """Create or open a Pipeline layer."""

        super().__init__(gpkgFile,
                         layerName,
                         styleName=PipelineLayer.STYLE)

        self._elevationLayerId = elevationLayer.id() if elevationLayer else None

    @property
    def elevationLayer(self):
        return QgsProject.instance().mapLayer(self._elevationLayerId) if self._elevationLayerId else None

    def wrapFeature(self, feature):
        return self.getFeatureType()(self, self.elevationLayer, feature)
