# -*- coding: utf-8 -*-
from ..features.paddock import Paddock
from .condition_table import ConditionTable
from .imported_feature_layer import ImportedFeatureLayer


class PaddockLayer(ImportedFeatureLayer):

    STYLE = "paddock"

    def getFeatureType(self):
        return Paddock

    def __init__(self, project, gpkgFile, layerName, conditionTable: ConditionTable):
        """Create or open a Paddock layer."""

        super().__init__(project, gpkgFile, layerName, styleName=PaddockLayer.STYLE)

        self.conditionTable = conditionTable

    def wrapFeature(self, feature):
        return self.getFeatureType()(self, self.conditionTable, feature)
