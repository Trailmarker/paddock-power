# -*- coding: utf-8 -*-
from qgis.gui import QgsMapTool

from ...models import WorkspaceMixin


class MapTool(WorkspaceMixin, QgsMapTool):
    """A QGIS map tool class with a couple of convenience methods and properties."""

    def __init__(self):
        WorkspaceMixin.__init__(self)
        QgsMapTool.__init__(self, self.workspace.iface.mapCanvas())

    @property
    def canvas(self):
        """Get the map canvas associated with the tool."""
        return self.workspace.iface.mapCanvas()

    def clear(self):
        """Clear any graphics content or cursor mode associated with the tool."""
        pass

    def dispose(self):
        """Completely delete or destroy all graphics objects or other state associated with the tool."""
        self.deactivate()
