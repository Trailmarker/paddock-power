# -*- coding: utf-8 -*-
from ..features.waterpoint import Waterpoint
from .elevation_layer import ElevationLayer
from .imported_feature_layer import ImportedFeatureLayer


class WaterpointLayer(ImportedFeatureLayer):

    NAME = "Waterpoints"
    STYLE = "waterpoint"

    def __init__(self,
                 workspaceFile,
                 elevationLayer: ElevationLayer):
        """Create or open a Waterpoint layer."""

        super().__init__(Waterpoint,
                         workspaceFile,
                         layerName=WaterpointLayer.NAME,
                         styleName=WaterpointLayer.STYLE)
        
        self.elevationLayer = elevationLayer

   