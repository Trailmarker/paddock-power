# -*- coding: utf-8 -*-
from qgis.gui import QgsMapTool
from qgis.utils import iface

class PaddockPowerMapTool(QgsMapTool):

    def __init__(self):
        super(PaddockPowerMapTool, self).__init__(iface.mapCanvas())

        self.canvas = iface.mapCanvas()

    def clear(self):
        """Clear any graphics content or cursor mode associated with the tool."""
        pass

    def destroy(self):
        """Completely delete or destroy all graphics objects or other state associated with the tool."""
        self.deactivate()