# -*- coding: utf-8 -*-
from qgis.utils import plugins

from ..utils import PLUGIN_FOLDER


class WorkspaceMixin:

    def __init__(self):
        self._workspace = None

    @property
    def plugin(self):
        f"""The current instance of the plugin."""
        return plugins[PLUGIN_FOLDER]

    @property
    def workspace(self):
        f"""The workspace we are connected to."""
        return self._workspace if self._workspace else self.plugin.workspace

    @workspace.setter
    def workspace(self, workspace):
        self._workspace = workspace

    @property
    def ready(self):
        return self.workspace and self.workspace.ready

    @property
    def timeframe(self):
        # TODO could be null …
        return self.workspace.timeframe
