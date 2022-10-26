# -*- coding: utf-8 -*-
from ..features.old_condition_record import OldConditionRecord
from .feature_layer import FeatureLayer


class OldConditionRecordLayer(FeatureLayer):

    # STYLE = "condition_record"
    @classmethod
    def getFeatureType(cls):
        return OldConditionRecord

    def __init__(self, gpkgFile, layerName):
        """Create or open a Waterpoint layer."""

        super().__init__(gpkgFile, layerName, styleName=None)
