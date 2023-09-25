# -*- coding: utf-8 -*-
from ...layers.fields import MetricPaddockSchema
from ..details import PaddockDetails, PaddockDetailsEdit
from .feature_table_action import FeatureTableAction
from .feature_table import FeatureTable


class PaddockTable(FeatureTable):

    def __init__(self, displayMode=False, parent=None):
        """Constructor."""

        super().__init__(MetricPaddockSchema, PaddockDetails, PaddockDetailsEdit, parent)

        self.displayMode = displayMode
        self.featureLayer = self.workspace.paddockLayer

    @property
    def supportedFeatureTableActions(self):
        return [FeatureTableAction.selectFeature, FeatureTableAction.viewFeatureDetails, FeatureTableAction.editFeature]
