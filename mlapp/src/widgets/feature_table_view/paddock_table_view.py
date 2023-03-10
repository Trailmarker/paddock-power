# -*- coding: utf-8 -*-
from ...layers.fields import Schema
from ...layers.fields.fields import *
from ..paddock_details import PaddockDetailsEdit
from .feature_table_action import FeatureTableAction
from .feature_table_view import FeatureTableView


PaddockTableViewSchema = Schema([AreaTitle,
                                 Status,
                                 WateredArea,
                                 EstimatedCapacityPerArea,
                                 EstimatedCapacity,
                                 PotentialCapacityPerArea,
                                 PotentialCapacity])


class PaddockTableView(FeatureTableView):

    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(PaddockTableViewSchema, PaddockDetailsEdit, parent)

        self.featureLayer = self.workspace.paddockLayer

    @property
    def supportedFeatureTableActions(self):
        return [FeatureTableAction.selectFeature, FeatureTableAction.editFeature]
