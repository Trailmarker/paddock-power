# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt

from qgis.gui import QgsAttributeTableFilterModel

from ...layers.fields import Timeframe, TIMEFRAME
from ...utils import qgsDebug


class FeatureTableFilterModel(QgsAttributeTableFilterModel):
    """A customisation of the QGIS attribute table filter model to filter features
    by their timeframe, if present."""

    def __init__(self, timeframe, canvas, sourceModel, parent=None):
        QgsAttributeTableFilterModel.__init__(self, canvas, sourceModel, parent)

        self._timeframe = timeframe
        self._timeframeColumn = self.sourceModel().columnFromFieldName(TIMEFRAME)

    def onTimeframeChanged(self, timeframe):
        """Handle the timeframe changing."""
        self._timeframe = timeframe
        self.invalidateFilter()

    def filterAcceptsRow(self, sourceModelRow, sourceParent):
        # Timeframe filtering only applies when no filteredFeatures have been set
        # qgsDebug(f"self.filterModee) == {self.filterMode()}")
        
        if self.filterMode() == QgsAttributeTableFilterModel.ShowFilteredList:
            return super().filterAcceptsRow(sourceModelRow, sourceParent)
      
        # The result when there is no 'Timeframe' column at all
        if self._timeframeColumn < 0:
            return True

        timeframeData = str(
            self.sourceModel().data(
                self.sourceModel().index(
                    sourceModelRow,
                    self._timeframeColumn,
                    sourceParent),
                Qt.DisplayRole))

        return (Timeframe[timeframeData] == Timeframe[self._timeframe.name])
