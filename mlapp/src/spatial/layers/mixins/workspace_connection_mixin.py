# -*- coding: utf-8 -*-
from abc import abstractproperty
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot


from ....utils import qgsError, qgsDebug
from ...fields.timeframe import Timeframe


class WorkspaceConnectionMixin:
    workspaceConnectionChanged = pyqtSignal()
    selectedFeatureChanged = pyqtSignal(type, int, bool)

    def __init__(self):
        super().__init__()

        self._workspace = None
        self._selectedFeature = None
        self._blockWorkspaceConnnection = False


    @abstractproperty
    def featureType(self):
        pass


    @property
    def connectedToWorkspace(self):
        """Are we both connected to the workspace and not temporarily blocked."""
        return self._workspace and not self._blockWorkspaceConnnection

    @property
    def workspace(self):
        f"""The workspace we are connected to."""
        return self._workspace

    @property
    def currentTimeframe(self):
        """Get the current timeframe for this layer (same as that of the workspace)."""
        return self.workspace.currentTimeframe if self.connectedToWorkspace else Timeframe.Undefined

    def connectWorkspace(self, workspace):
        """Hook it up to uor veins."""
        self._workspace = workspace
        self.workspaceConnectionChanged.emit()

    def workspaceLayer(self, layerType):
        """Get a layer we depend on to work with by type."""
        if self.connectedToWorkspace:
            return self.workspace.workspaceLayers.layer(layerType)
        else:
            qgsError(f"{self.typeName}.workspaceLayer({layerType}): no workspace connection")


    def selectFeature(self, feature):
        """Select a Feature."""
        pass
        # self.selectedFeatureChanged.emit(self.featureType, feature.FID, feature.focusOnSelect())

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

    @pyqtSlot(Timeframe)
    def onCurrentTimeframeChanged(self, timeframe):
        """Handle the current timeframe changing."""
        self.currentTimeframeChanged.emit(timeframe)

    @pyqtSlot()
    def onWorkspaceConnectionChanged(self):
        """Handle the workspace changing."""
        qgsDebug(f"{self.typeName}.onWorkspaceConnectionChanged(): {self.workspace}")
        if self.workspace:
            self.workspace.selectedFeaturesChanged.connect(self.onSelectedFeaturesChanged)
            self.workspace.currentTimeframeChanged.connect(self.onCurrentTimeframeChanged)
            self.currentTimeframeChanged.connect(self.workspace.setCurrentTimeframe)

    