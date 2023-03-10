# -*- coding: utf-8 -*-
from ...layers.fields.table_view_schemas import PaddockTableViewSchema
from ..paddock_details.paddock_details_edit import PaddockDetailsEdit
from .feature_table_view import FeatureTableView


class PaddockTableView(FeatureTableView):

    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(PaddockTableViewSchema, PaddockDetailsEdit, parent)

        self.featureLayer = self.workspace.paddockLayer
