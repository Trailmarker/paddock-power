# -*- coding: utf-8 -*-
from ...layers.fields import FenceSchema
from ..details import FenceDetailsEdit
from .feature_table_action import FeatureTableAction
from .feature_table import FeatureTable


class FenceTable(FeatureTable):

    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(FenceSchema, None, FenceDetailsEdit, parent)
        self.featureLayer = self.workspace.fenceLayer

    @property
    def supportedFeatureTableActions(self):
        return list(FeatureTableAction)
