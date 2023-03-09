# -*- coding: utf-8 -*-

from .feature_layer_table_view import FeatureLayerTableView

class PaddockLayerTableView(FeatureLayerTableView):

    def __init__(self, parent=None):
        """Constructor."""
        
        super().__init__(parent)
        self.featureLayer = self.workspace.paddockLayer
