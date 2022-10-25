# -*- coding: utf-8 -*-
from qgis.gui import QgsMapTool


class MapTool(QgsMapTool):

    def __init__(self, canvas):
        super().__init__(canvas)

        self.canvas = canvas

    def clear(self):
        """Clear any graphics content or cursor mode associated with the tool."""
        pass

    def dispose(self):
        """Completely delete or destroy all graphics objects or other state associated with the tool."""
        self.deactivate()
