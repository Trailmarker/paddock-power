# -*- coding: utf-8 -*-
import os.path
import sys

from qgis.PyQt.QtCore import QCoreApplication, QObject, QSettings, QTranslator, pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from qgis.core import QgsApplication, QgsProject

from .resources_rc import *

from .src.models.glitch import Glitch
from .src.models.project import Project
from .src.provider import Provider
from .src.utils import qgsInfo, resolveGeoPackageFile, PLUGIN_NAME


class PaddockPower(QObject):

    __GLITCH_HOOK_WRAPPER = "__glitchHookWrapper"

    caughtGlitch = pyqtSignal(Glitch)

    def __init__(self, iface):
        super().__init__()

        self.iface = iface
        self.actions = []

        self.setupGlitchHook()
        self.caughtGlitch.connect(Glitch.popup)

        # Initialise locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(
            os.path.dirname(__file__),
            "i18n",
            f"PaddockPower_{locale}.qm")

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)
            QCoreApplication.installTranslator(self.translator)

        self.provider = Provider()
        QgsApplication.processingRegistry().addProvider(self.provider)

        QgsProject.instance().cleared.connect(self.unloadProject)
        QgsProject.instance().readProject.connect(self.detectProject)

        self.project = None

    def addAction(self,
                  icon,
                  text,
                  callback,
                  enabled=True,
                  addToMenu=False,
                  addToToolbar=True,
                  statusTip=None,
                  whatsThis=None,
                  parent=None):

        icon = QIcon(icon)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled)

        if statusTip is not None:
            action.setStatusTip(statusTip)
        if whatsThis is not None:
            action.setWhatsThis(whatsThis)
        if addToToolbar:
            self.toolbar.addAction(action)
        if addToMenu:
            self.iface.addPluginToMenu(self.menu, action)
        self.actions.append(action)
        return action

    def initGui(self):
        """The real Paddock Power GUI is initialised when a project is opened,
           but QGIS utilities call this when the plug-in is loaded anyway."""
        # Initialise plug-in menu and toolbar
        self.menu = Project.MENU_NAME

        self.toolbar = self.iface.addToolBar(u"PaddockPower")
        self.toolbar.setObjectName(u"PaddockPower")

        self.actions = []

        self.addAction(
            QIcon(":/plugins/mlapp/images/paddock.png"),
            text=u"View Paddocks",
            callback=self.openPaddockView,
            parent=self.iface.mainWindow())

        self.addAction(
            QIcon(":/plugins/mlapp/images/split-paddock.png"),
            text=u"Plan Fences",
            callback=self.openFenceView,
            parent=self.iface.mainWindow())

        self.addAction(
            QIcon(":/plugins/mlapp/images/split-paddock.png"),
            text=u"Plan Pipelines",
            callback=self.openPipelineView,
            parent=self.iface.mainWindow())
        
        self.addAction(
            QIcon(":/plugins/mlapp/images/split-paddock.png"),
            text=u"Plan Waterpoints",
            callback=self.openWaterpointView,
            parent=self.iface.mainWindow())

        self.detectProject()

    # Override Glitch type exceptions application-wide
    def setupGlitchHook(self):
        if hasattr(sys.excepthook, PaddockPower.__GLITCH_HOOK_WRAPPER):
            qgsInfo("GlitchHook: Glitch hook already set.")
            return

        exceptHook = sys.excepthook
        qgsInfo("GlitchHook: setting up Glitch hook.")

        def glitchHookWrapper(exceptionType, e, traceback):
            if isinstance(e, Glitch):
                self.caughtGlitch.emit(e)
                return
            else:
                exceptHook(exceptionType, e, traceback)

        setattr(glitchHookWrapper, PaddockPower.__GLITCH_HOOK_WRAPPER, sys.excepthook)
        sys.excepthook = glitchHookWrapper

    @staticmethod
    def restoreSystemExceptionHook():
        if hasattr(sys.excepthook, PaddockPower.__GLITCH_HOOK_WRAPPER):
            qgsInfo("GlitchHook: restoring original system exception hook.")
            sys.excepthook = getattr(sys.excepthook, PaddockPower.__GLITCH_HOOK_WRAPPER)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS interface."""
        try:
            QgsProject.instance().cleared.disconnect(self.unloadProject)
            QgsProject.instance().readProject.disconnect(self.detectProject)
        except BaseException:
            pass

        try:
            self.unloadProject()
        except BaseException:
            pass

        try:
            # Remove the plugin menu item and icon
            for action in self.actions:
                self.iface.removePluginMenu(Project.MENU_NAME, action)
                self.iface.removeToolBarIcon(action)

            # Remove the toolbar
            del self.toolbar
        except BaseException:
            pass

        try:
            # Remove processing provider
            QgsApplication.processingRegistry().removeProvider(self.provider)
        except BaseException:
            pass

        PaddockPower.restoreSystemExceptionHook()

    @Glitch.glitchy(f"An exception occurred while trying to detect a {PLUGIN_NAME} project.")
    def detectProject(self, _=None):
        """Detect a Paddock Power project in the current QGIS project."""
        self.project = None
        try:
            gpkgFile = resolveGeoPackageFile()
            if gpkgFile is not None:
                qgsInfo("Paddock Power loading project …")
                self.project = Project(self.iface, gpkgFile)
            else:
                qgsInfo("Paddock Power no GeoPackage file …")
        except BaseException:
            pass
        if self.project is not None:
            self.project.addToMap()

    def unloadProject(self):
        """Removes the plugin menu item and icon from QGIS interface."""
        if self.project is not None:
            qgsInfo("Paddock Power unloading project …")
            self.project.unload()
            self.project = None

    def openFenceView(self):
        if self.project is not None:
            self.project.openFenceView()

    def openPaddockView(self):
        if self.project is not None:
            self.project.openPaddockView()

    def openPipelineView(self):
        if self.project is not None:
            self.project.openPipelineView()
   
    def openWaterpointView(self):
        if self.project is not None:
            self.project.openWaterpointView()
