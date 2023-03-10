# -*- coding: utf-8 -*-
from ...layers.fields import Schema
from ...layers.fields.fields import *
from ..pipeline_details import PipelineDetailsEdit
from .feature_table_view import FeatureTableView

PipelineTableViewSchema = Schema([LengthTitle,
                                  Status])


class PipelineTableView(FeatureTableView):

    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(PipelineTableViewSchema, PipelineDetailsEdit, parent)
        self.featureLayer = self.workspace.pipelineLayer
