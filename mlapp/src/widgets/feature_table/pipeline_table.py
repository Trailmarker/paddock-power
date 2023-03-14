# -*- coding: utf-8 -*-
from ...layers.fields import PipelineSchema
from ..details import PipelineDetailsEdit
from .feature_table import FeatureTable
from .feature_table_action import FeatureTableAction

# PipelineTableSchema = Schema([LengthTitle,
#                                   Status])


class PipelineTable(FeatureTable):

    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(PipelineSchema, None, PipelineDetailsEdit, parent)
        self.featureLayer = self.workspace.pipelineLayer

    @property
    def supportedFeatureTableActions(self):
        return list(FeatureTableAction)
