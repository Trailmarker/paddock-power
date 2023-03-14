# -*- coding: utf-8 -*-
from ...layers.fields import BasePaddockSchema
from .feature_table_action import FeatureTableAction
from .feature_table import FeatureTable


# BasePaddockTableSchema = Schema([AreaTitle, Status])


class BasePaddockTable(FeatureTable):

    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(BasePaddockSchema, None, None, parent)

        self.featureLayer = self.workspace.basePaddockLayer

    @property
    def supportedFeatureTableActions(self):
        return [FeatureTableAction.selectFeature]
