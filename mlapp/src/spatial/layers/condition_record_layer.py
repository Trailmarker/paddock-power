# -*- coding: utf-8 -*-
from ..features.condition_record import ConditionRecord
from .feature_layer import FeatureLayer


class ConditionRecordLayer(FeatureLayer):

    # STYLE = "condition_record"
    @classmethod
    def getFeatureType(cls):
        return ConditionRecord

    def __init__(self, gpkgFile, layerName):
        """Create or open a Waterpoint layer."""

        super().__init__(gpkgFile, layerName, styleName=None)
