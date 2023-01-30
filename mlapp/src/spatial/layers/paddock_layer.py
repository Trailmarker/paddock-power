# -*- coding: utf-8 -*-
from ..features.paddock import Paddock
from .condition_table import ConditionTable
from .imported_feature_layer import ImportedFeatureLayer


class PaddockLayer(ImportedFeatureLayer):

    NAME = "Paddocks"
    STYLE = "paddock"

    @classmethod
    def getFeatureType(cls):
        return Paddock

    def __init__(self,
                 workspaceFile: str,
                 conditionTable: ConditionTable):
        """Create or open a Paddock layer."""

        super().__init__(workspaceFile,
                         layerName=PaddockLayer.NAME,
                         styleName=PaddockLayer.STYLE)

        self.conditionTable = conditionTable

