# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot


from ....utils import qgsError, qgsDebug


class WorkspaceConnectionMixin:

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

    def connectWorkspace(self, workspace):
        """Hook it up to uor veins."""
        self._workspace = workspace
        self.onWorkspaceConnectionChanged()

    def workspaceLayer(self, layerType):
        """Get a layer we depend on to work with by type."""
        if self.connectedToWorkspace:
            return self.workspace.workspaceLayers.layer(layerType)
        else:
            qgsError(f"{type(self).__name__}.workspaceLayer({layerType}): no workspace connection")
            return None

    def onWorkspaceConnectionChanged(self):
        """Handle the workspace changing."""
        pass