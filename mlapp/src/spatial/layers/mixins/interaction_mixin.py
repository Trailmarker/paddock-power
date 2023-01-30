# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot

from ....utils import qgsDebug
from ...features.feature import Feature
from ...fields.timeframe import Timeframe
from ...layers.mixins.workspace_connection_mixin import WorkspaceConnectionMixin


class InteractionMixin(WorkspaceConnectionMixin):
    featureLayerSelected = pyqtSignal(type, type)
    timeframeChanged = pyqtSignal(Timeframe)

    def __init__(self):
        super().__init__()

        self._selectedFeature = None

    def getFeatureType(self):
        """Return the Feature type with which this mixin will interact."""
        pass

    @property
    def timeframe(self):
        """Get the current timeframe for this layer (same as that of the workspace)."""
        return self.workspace.timeframe if self.connectedToWorkspace else Timeframe.Undefined

    @pyqtSlot(type, type)
    def onSelectedFeatureChanged(self, layerType, featureType):
        """Handle a change in the selected Feature."""

        # If featureType is None, then we're clearing the selection on instruction
        if not issubclass(featureType, Feature):
            qgsDebug(f"{featureType.__name__} is not a Feature subclass")
            self.removeSelection()
            return

        ourFeature = (featureType == self.getFeatureType())

        # Are we going to focus based on this new Feature?
        if not ourFeature:
            if featureType.focusOnSelect():
                qgsDebug(f"{featureType.__name__} is not our Feature type {self.getFeatureType().__name__}")
                self.removeSelection()
            return

        if ourFeature:
            if self.connectedToWorkspace:
                self.changeSelection(self.workspace.selectedFeature)
            return

    def removeSelection(self):
        """Clear the selected Feature."""
        if self._selectedFeature:
            self._selectedFeature.onDeselectFeature()
        self._selectedFeature = None

    def changeSelection(self, feature):
        """Select a Feature."""
        self.removeSelection()
        self._selectedFeature = feature
        self._selectedFeature.onSelectFeature()
        self.featureLayerSelected.emit(type(feature.featureLayer), type(feature))

    @pyqtSlot(Timeframe)
    def onCurrentTimeframeChanged(self, timeframe):
        """Handle the current timeframe changing."""
        self.timeframeChanged.emit(timeframe)

    def onWorkspaceConnectionChanged(self):
        super().onWorkspaceConnectionChanged()

        if self.workspace:
            qgsDebug(f"{self.__class__.__name__} connected to {self.workspace}")
            self.workspace.featureLayerSelected.connect(self.onSelectedFeatureChanged)
            self.workspace.timeframeChanged.connect(self.onCurrentTimeframeChanged)
            #self.timeframeChanged.connect(self.workspace.setCurrentTimeframe)
