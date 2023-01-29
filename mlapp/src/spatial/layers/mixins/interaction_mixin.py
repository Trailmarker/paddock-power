# -*- coding: utf-8 -*-
from abc import abstractproperty
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot


from ...fields.timeframe import Timeframe
from ...layers.mixins.workspace_connection_mixin import WorkspaceConnectionMixin


class InteractionMixin(WorkspaceConnectionMixin):
    selectedFeatureChanged = pyqtSignal(type, int, bool)

    def __init__(self):
        super().__init__()

        self._selectedFeature = None

    @abstractproperty
    def featureType(self):
        pass

    @property
    def currentTimeframe(self):
        """Get the current timeframe for this layer (same as that of the workspace)."""
        return self.workspace.currentTimeframe if self.connectedToWorkspace else Timeframe.Undefined

    @pyqtSlot(type, int, bool)
    def onSelectedFeatureChanged(self, featureLayerType, fid, focusOnSelect):
        """Handle a change in the selected Feature."""

        # If featureType is None, then we're clearing the selection on instruction
        if isinstance(None, featureLayerType) or isinstance(None, featureLayerType):
            if focusOnSelect:
                self.removeSelection()
            return

        # If the incoming Feature type is not ours, and demands focus, then clear our selection
        if featureLayerType != self.featureType and focusOnSelect:
            self.removeSelection()
            return

        if not self.connectedToWorkspace:
            return

        self._blockWorkspaceConnnection = True

        try:
            # Was something selected?
            hadSelection = self._selectedFeature is not None

            # Is this our Feature?
            ourFeature = featureLayerType == self.featureType

            # Are we going to focus based on this new Feature?
            if not ourFeature:
                if focusOnSelect:
                    self.removeSelection()
                return

            if ourFeature:
                # Is it the same one that's already selected?
                if hadSelection and (self._selectedFeature.FID == fid):
                    return

                feature = self.workspaceLayer(featureLayerType).getFeature(fid)
                self.changeSelection(feature)
                return
        finally:
            self._blockWorkspaceConnnection = False

    def removeSelection(self):
        """Clear the selected Feature."""
        self._selectedFeature = None

    def changeSelection(self, feature):
        """Select a Feature."""
        if self._selectedFeature:
            self._selectedFeature.onDeselectFeature()
        self._selectedFeature = feature
        self.selectedFeatureChanged.emit(self.featureType, feature.FID, feature.focusOnSelect())

    @pyqtSlot(Timeframe)
    def onCurrentTimeframeChanged(self, timeframe):
        """Handle the current timeframe changing."""
        self.currentTimeframeChanged.emit(timeframe)
