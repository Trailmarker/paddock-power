# -*- coding: utf-8 -*-
from ...layers.fields import Schema
from ...layers.fields.fields import *
from ..fence_details import FenceDetailsEdit
from .feature_table_view import FeatureTableView

FenceTableViewSchema = Schema([LengthTitle,
                               BuildOrder,
                               Status,
                               Length])


class FenceTableView(FeatureTableView):

    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(FenceTableViewSchema, FenceDetailsEdit, parent)
        self.featureLayer = self.workspace.fenceLayer
