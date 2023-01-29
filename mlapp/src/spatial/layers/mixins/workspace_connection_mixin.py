# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot


from ....utils import qgsError
from ...fields.timeframe import Timeframe


class WorkspaceConnectionMixin:
    workspaceConnectionChanged = pyqtSignal()

    def __init__(self):
        super().__init__()

        self._workspace = None
        self._blockWorkspaceConnnection = False

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

    @pyqtSlot(Timeframe)
    def onCurrentTimeframeChanged(self, timeframe):
        """Handle the current timeframe changing."""
        self.triggerRepaint(deferredUpdate=False)
        self.currentTimeframeChanged.emit(timeframe)

    @pyqtSlot()
    def onWorkspaceConnectionChanged(self):
        """Handle the workspace changing."""

        if self.workspace:
            self.workspace.selectedFeaturesChanged.connect(self.onSelectedFeaturesChanged)
            self.workspace.currentTimeframeChanged.connect(self.onCurrentTimeframeChanged)
            self.currentTimeframeChanged.connect(self.workspace.setCurrentTimeframe)
