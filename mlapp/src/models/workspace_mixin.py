# -*- coding: utf-8 -*-
from functools import cached_property
from qgis.utils import plugins


class WorkspaceMixin:

    def __init__(self):
        super().__init__()
        
    @cached_property
    def plugin(self):
        return plugins['mlapp']

    @property
    def workspace(self):
        f"""The workspace we are connected to."""
        return self.plugin.workspace

    @property
    def ready(self):
        return self.workspace and self.workspace.ready

    @property
    def timeframe(self):
        # TODO could be null …
        return self.workspace.timeframe
