# -*- coding: utf-8 -*-
from abc import abstractproperty

from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot

from ..mixins.workspace_connection_mixin import WorkspaceConnectionMixin


class SelectedFeaturesMixin(WorkspaceConnectionMixin):

   
  

    @pyqtSlot(type, int, bool)
    def onSelectedFeaturesChanged(self, featureLayerType, fid, changeSelection=True):
        """Handle a change in the selected Feature."""

        # If featureType is None, then we're clearing the selection
        if featureLayerType != self.featureType and self.featureType.focusOnSelect():
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
                if featureLayerType.focusOnSelect():
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
