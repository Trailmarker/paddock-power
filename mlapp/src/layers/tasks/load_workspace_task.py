# -*- coding: utf-8 -*-

from qgis.core import QgsTask

from ...utils import PLUGIN_NAME, guiStatusBarAndInfo, qgsInfo


class LoadWorkspaceTask(QgsTask):

    def __init__(self, iface, workspaceFile):
        """Input is a Workspace."""
        super().__init__(
            f"{PLUGIN_NAME} Load Workspace(workspaceFile={workspaceFile})",
            flags=QgsTask.CanCancel | QgsTask.CancelWithoutPrompt)

        self.iface = iface
        self.workspaceFile = workspaceFile

    def run(self):
        f"""Load all layers in a {PLUGIN_NAME} workspace."""
        raise NotImplementedError

    def finished(self, result):
        """Called when task completes (successfully or otherwise)."""
        self.workspace.onTaskCompleted(self, result)

    def cancel(self):
        super().cancel()
