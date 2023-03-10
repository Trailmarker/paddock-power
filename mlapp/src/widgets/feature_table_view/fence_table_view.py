# -*- coding: utf-8 -*-

from .feature_table_view import FeatureTableView


class FenceTableView(FeatureTableView):

    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(parent)
        self.featureLayer = self.workspace.fenceLayer
