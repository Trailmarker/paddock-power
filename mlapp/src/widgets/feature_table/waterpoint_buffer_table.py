# -*- coding: utf-8 -*-
from ...layers.fields import WaterpointBufferSchema
from .feature_table_action.feature_table_action import FeatureTableAction
from .feature_table import FeatureTable


class WaterpointBufferTable(FeatureTable):

    def __init__(self, parent=None):
        """Constructor."""

        super().__init__(WaterpointBufferSchema, None, None, parent)

    @property
    def supportedFeatureTableActions(self):
        return [FeatureTableAction.selectFeature]
