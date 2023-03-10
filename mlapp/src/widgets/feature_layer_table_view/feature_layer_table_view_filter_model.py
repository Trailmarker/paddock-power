# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt

from qgis.gui import QgsAttributeTableFilterModel

from ...layers.fields import Timeframe, TIMEFRAME
from ...utils import qgsDebug

class FeatureLayerTableViewFilterModel(QgsAttributeTableFilterModel):

    def __init__(self, workspace, schema, canvas, sourceModel, parent=None):
        QgsAttributeTableFilterModel.__init__(self, canvas, sourceModel, parent)

        self._workspace = workspace
        
        # self._displaySchema = schema
        
        self._timeframeColumnIndex = self.sourceModel().columnIndexFromFieldName(TIMEFRAME)
        
        # qgsDebug(f"Display field names = {self._displaySchema.displayFieldNames()}")

    # def filterAcceptsColumn(self, sourceModelColumn, sourceModelIndex):
    #     accept = super().filterAcceptsColumn(sourceModelColumn, sourceModelIndex)
        
    #     if not accept:
    #         return False

    #     field = self.sourceModel().layer().fields()[sourceModelColumn]
        
    #     qgsDebug(f"Filtering field {field.name()} = {field.name() in self._displaySchema.displayFieldNames()}")
        
    #     return accept and (field.name() in self._displaySchema.displayFieldNames())

    def filterAcceptsRow(self, sourceModelRow, sourceParent):
        accept = super().filterAcceptsRow(sourceModelRow, sourceParent)
        
        if not accept:
            return False
        
        timeframeData = str(self.sourceModel().data(self.sourceModel().index(sourceModelRow, self._timeframeColumnIndex, sourceParent), Qt.DisplayRole))
        
        qgsDebug(f"Filtering row {sourceModelRow}, timeframeData = {timeframeData}, timeframe = {self._workspace.timeframe.name}")
        
        return accept and (Timeframe[timeframeData] == Timeframe[self._workspace.timeframe.name])
