# -*- coding: utf-8 -*-
from ..features.paddock import Paddock
from ..fields.schemas import PaddockSchema
from .condition_table import ConditionTable
from .imported_feature_layer import ImportedFeatureLayer


class PaddockLayer(ImportedFeatureLayer):

    NAME = "Paddocks"
    STYLE = "paddock"

    def __init__(self,
                 workspaceFile: str,
                 conditionTable: ConditionTable):
        """Create or open a Paddock layer."""

        super().__init__(Paddock,
                         workspaceFile,
                         layerName=PaddockLayer.NAME,
                         styleName=PaddockLayer.STYLE)

        self.conditionTable = conditionTable

    def getSchema(self):
        """Return the Schema for this layer."""
        return PaddockSchema

    def getWkbType(self):
        """Return the WKB type for this layer."""
        return PaddockSchema.wkbType
