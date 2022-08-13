# -*- coding: utf-8 -*-
from qgis.core import Qgis, QgsMessageLog

def qgsDebug(message, tag="", level=Qgis.Info):
    """Print a debug message."""
    QgsMessageLog.logMessage(
        message, tag=tag, level=level)
