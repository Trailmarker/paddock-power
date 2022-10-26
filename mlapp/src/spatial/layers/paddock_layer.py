# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ..features.edits import Edits
from ..features.paddock import Paddock
from .old_condition_record_layer import OldConditionRecordLayer
from .land_system_layer import LandSystemLayer
from .status_feature_layer import StatusFeatureLayer
from .waterpoint_buffer_layer import WaterpointBufferLayer


class PaddockLayer(StatusFeatureLayer):

    STYLE = "paddock"

    @classmethod
    def getFeatureType(cls):
        return Paddock

    def __init__(self, gpkgFile, layerName, landSystemLayer: LandSystemLayer,
                 waterpointBufferLayer: WaterpointBufferLayer, conditionRecordLayer: OldConditionRecordLayer):
        """Create or open a Paddock layer."""

        super().__init__(gpkgFile, layerName, styleName=PaddockLayer.STYLE)

        self._landSystemLayerId = landSystemLayer.id()
        self._waterpointBufferLayerId = waterpointBufferLayer.id()
        self._conditionRecordLayerId = conditionRecordLayer.id()

    @property
    def landSystemLayer(self):
        return QgsProject.instance().mapLayer(self._landSystemLayerId)

    @property
    def waterpointBufferLayer(self):
        return QgsProject.instance().mapLayer(self._waterpointBufferLayerId)

    @property
    def conditionRecordLayer(self):
        return QgsProject.instance().mapLayer(self._conditionRecordLayerId)

    def wrapFeature(self, feature):
        return self.getFeatureType()(self, self.landSystemLayer, self.waterpointBufferLayer, self.conditionRecordLayer, feature)

    @Edits.persistEdits
    def analyseFeatures(self):
        edits = Edits()

        for paddock in self.getFeatures():
            edits.editBefore(paddock.analyseFeature())
        
        return edits