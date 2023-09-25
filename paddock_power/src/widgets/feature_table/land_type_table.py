# -*- coding: utf-8 -*-
from ...layers.fields import LandTypeSchema
from ..details import LandTypeDetails, LandTypeDetailsEdit
from .feature_table_action import FeatureTableAction
from .feature_table import FeatureTable


class LandTypeTable(FeatureTable):

    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(LandTypeSchema, LandTypeDetails, LandTypeDetailsEdit, parent)

        self.featureLayer = self.workspace.landTypeLayer

    @property
    def supportedFeatureTableActions(self):
        return [FeatureTableAction.selectFeature, FeatureTableAction.viewFeatureDetails, FeatureTableAction.editFeature]
