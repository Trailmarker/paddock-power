# -*- coding: utf-8 -*-
from ...layers.fields import MetricPaddockSchema
from ...layers.fields.fields import *
from ..paddock_details import PaddockDetails, PaddockDetailsEdit
from .feature_table_action import FeatureTableAction
from .feature_table import FeatureTable


# PaddockTableSchema = Schema([AreaTitle,
#                                  Status,
#                                  WateredArea,
#                                  EstimatedCapacityPerArea,
#                                  EstimatedCapacity,
#                                  PotentialCapacityPerArea,
#                                  PotentialCapacity])


class PaddockTable(FeatureTable):

    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(MetricPaddockSchema, PaddockDetails, PaddockDetailsEdit, parent)

        self.featureLayer = self.workspace.paddockLayer

    @property
    def supportedFeatureTableActions(self):
        return [FeatureTableAction.selectFeature, FeatureTableAction.editFeature]
