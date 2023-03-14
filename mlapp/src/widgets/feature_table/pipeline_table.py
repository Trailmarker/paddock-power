# -*- coding: utf-8 -*-
from ...layers.fields import PipelineSchema
from ...layers.fields.fields import *
from ..pipeline_details import PipelineDetailsEdit
from .feature_table_action import FeatureTableAction
from .feature_table import FeatureTable

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
