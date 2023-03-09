# -*- coding: utf-8 -*-

from .feature_layer_table_view import FeatureLayerTableView

class FenceLayerTableView(FeatureLayerTableView):

    def __init__(self, parent=None):
        """Constructor."""
        
        super().__init__(parent)
        self.featureLayer = self.workspace.fenceLayer
