# -*- coding: utf-8 -*-
from ...layers.fields import WaterpointSchema
from ..details import WaterpointDetails, WaterpointDetailsEdit
from .feature_table_action.feature_table_action import FeatureTableAction
from .feature_table import FeatureTable


class WaterpointTable(FeatureTable):

    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(WaterpointSchema, WaterpointDetails, WaterpointDetailsEdit, parent)
        self.featureLayer = self.workspace.waterpointLayer

    @property
    def supportedFeatureTableActions(self):
        return [FeatureTableAction.selectFeature, FeatureTableAction.viewFeatureDetails, FeatureTableAction.editFeature,
                FeatureTableAction.undoTrashFeature, FeatureTableAction.planBuildFeature]
