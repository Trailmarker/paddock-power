# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsProject

from ..utils import resolveGeoPackageFile, PLUGIN_NAME
from .glitch import Glitch
from .glitch_hook import GlitchHook
from .project import Project
from .singleton import Singleton


class State(GlitchHook):
    PLUGIN_NAME = "MLA Paddock Power"

    unloading = pyqtSignal()

    def __init__(self):
        super().__init__()

    @Glitch.glitchy(f"An exception occurred while trying to detect an {PLUGIN_NAME} project.")
    def detectState(self):
        """Detect a Paddock Power project in the current QGIS project."""
        self.project = None
        try:
            gpkgFile = resolveGeoPackageFile()
            if gpkgFile is not None:
                self.project = Project(gpkgFile)
                self.unloading.connect(self.project.unload)
        except BaseException:
            pass
        if self.project is not None:
            self.project.addToMap()

    def unload(self):
        """Clear the current Project, for example if the current QGIS project is closed."""
