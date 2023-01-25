# -*- coding: utf-8 -*-
import os.path
import sys

from qgis.PyQt.QtCore import QCoreApplication, QObject, QSettings, QTranslator, pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from qgis.core import QgsExpression, QgsProject

from .resources_rc import *

from .src.paddock_power_functions import PaddockPowerFunctions
from .src.models.glitch import Glitch
from .src.models.project import Project
from .src.utils import guiError, qgsInfo, resolveGeoPackageFile, resolveProjectFile, PLUGIN_FOLDER, PLUGIN_NAME


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

        # Register QGIS expression extensions (used in symbology etc)
        self.registerFunctions()

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
            QIcon(f":/plugins/{PLUGIN_FOLDER}/images/paddock-power.png"),
            text=f"Open {PLUGIN_NAME} …",
            callback=self.openFeatureView,
            parent=self.iface.mainWindow())

        self.addAction(
            QIcon(f":/plugins/{PLUGIN_FOLDER}/images/refresh-paddock-power.png"),
            text=f"Refresh {PLUGIN_NAME} Project …",
            callback=lambda *_: self.detectProject(),
            parent=self.iface.mainWindow())

        self.addAction(
            QIcon(f":/plugins/{PLUGIN_FOLDER}/images/new-paddock-power.png"),
            text=f"Create {PLUGIN_NAME} Project …",
            callback=lambda *_: self.createProject(),
            parent=self.iface.mainWindow())

        self.addAction(
            QIcon(f":/plugins/{PLUGIN_FOLDER}/images/import.png"),
            text=f"Import {PLUGIN_NAME} Data …",
            callback=lambda *_: self.importData(),
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
            # Unregister the extension functions
            self.unregisterFunctions()
        except BaseException:
            pass

        PaddockPower.restoreSystemExceptionHook()

    def registerFunctions(self):
        f"""Register the extension functions used by {PLUGIN_NAME}."""
        for paddockPowerFunction in PaddockPowerFunctions:
            QgsExpression.registerFunction(paddockPowerFunction)

    def unregisterFunctions(self):
        f"""Register the extension functions used by {PLUGIN_NAME}."""
        for paddockPowerFunction in PaddockPowerFunctions:
            QgsExpression.unregisterFunction(paddockPowerFunction)

    # @Glitch.glitchy(f"An exception occurred while trying to detect a {PLUGIN_NAME} project.")

    def detectProject(self, _=None):
        f"""Detect a {PLUGIN_NAME} Project in the current QGIS project."""

        self.project = None
        # try:
        projectFile = resolveProjectFile()
        if projectFile is None:
            qgsInfo(f"{PLUGIN_NAME} no QGIS project file located …")
        else:
            gpkgFile = resolveGeoPackageFile()
            if gpkgFile is not None and os.path.exists(gpkgFile):
                qgsInfo(f"{PLUGIN_NAME} loading project …")
                self.project = Project(self.iface, gpkgFile)
            else:
                qgsInfo(f"{PLUGIN_NAME} no GeoPackage file located …")
        # except BaseException as e:
        #     qgsInfo(f"{PLUGIN_NAME} exception occurred detecting project:")
        #     qgsInfo(f"{e}")

        if self.project is not None:
            self.project.addToMap()
        else:
            qgsInfo(f"{PLUGIN_NAME} no project detected …")

    # @Glitch.glitchy(f"An exception occurred while trying to create a {PLUGIN_NAME} project.")
    def createProject(self):
        f"""Create a new {PLUGIN_NAME} Project in the current QGIS project."""
        self.unloadProject()
        try:
            projectFile = resolveProjectFile()
            if projectFile is None:
                qgsInfo(f"{PLUGIN_NAME} no QGIS project file located …")
                guiError(f"Please create and save a QGIS project before you try to create a {PLUGIN_NAME} project.")
                return
            else:
                gpkgFile = resolveGeoPackageFile()
                if gpkgFile is not None:
                    if os.path.exists(gpkgFile):
                        qgsInfo(f"{PLUGIN_NAME} GeoPackage file already exists, not creating project …")
                        guiError(
                            f"A {PLUGIN_NAME} project already exists in the filesystem adjacent to your QGIS project file.")
                    else:
                        qgsInfo(f"{PLUGIN_NAME} creating project …")
                        self.project = Project(self.iface, gpkgFile)
                else:
                    qgsInfo(f"{PLUGIN_NAME} no GeoPackage file located …")
        except BaseException as e:
            qgsInfo(f"{PLUGIN_NAME} exception occurred creating project …")
            qgsInfo(str(e))
            pass

        if self.project is not None:
            self.project.addToMap()

    def importData(self):
        if self.project is not None:
            self.project.importData()

    def unloadProject(self):
        """Removes the plugin menu item and icon from QGIS interface."""
        if self.project is not None:
            qgsInfo(f"{PLUGIN_NAME} unloading project …")
            self.project.unload()
            self.project = None

    def openFeatureView(self):
        if self.project is not None:
            self.project.openFeatureView()
