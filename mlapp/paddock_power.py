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
from .src.models.container import Container
from .src.utils import guiError, guiInformation, guiWarning, qgsException, qgsInfo, resolveWorkspaceFile, resolveProjectFile, PLUGIN_FOLDER, PLUGIN_NAME


class PaddockPower(QObject):

    MENU_NAME = f"&{PLUGIN_NAME}"

    __GLITCH_HOOK_WRAPPER = "__glitchHookWrapper"

    caughtGlitch = pyqtSignal(Glitch)

    def __init__(self, iface):
        super().__init__()

        self.workspace = None

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

        self.container = None
        self.initContainer()

        QgsProject.instance().cleared.connect(self.unloadWorkspace)
        QgsProject.instance().readProject.connect(self.detectWorkspace)

    def initContainer(self):
        """Initialise the IoC container."""
        self.container = Container()
        self.container.init_resources()
        self.container.wire(modules=[__name__])

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
        """The real Paddock Power GUI is initialised when a QGIS project is opened,
           but QGIS utilities call this when the plug-in is loaded anyway."""
        # Initialise plug-in menu and toolbar
        self.menu = PaddockPower.MENU_NAME

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
            text=f"Refresh {PLUGIN_NAME} workspace …",
            callback=lambda *_: self.detectWorkspace(warning=True),
            parent=self.iface.mainWindow())

        self.addAction(
            QIcon(f":/plugins/{PLUGIN_FOLDER}/images/new-paddock-power.png"),
            text=f"Create {PLUGIN_NAME} workspace …",
            callback=lambda *_: self.createWorkspace(),
            parent=self.iface.mainWindow())

        self.addAction(
            QIcon(f":/plugins/{PLUGIN_FOLDER}/images/import.png"),
            text=f"Import {PLUGIN_NAME} Data …",
            callback=lambda *_: self.importData(),
            parent=self.iface.mainWindow())

        self.detectWorkspace()

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
            QgsProject.instance().cleared.disconnect(self.unloadWorkspace)
            QgsProject.instance().readProject.disconnect(self.detectWorkspace)
        except BaseException:
            pass

        try:
            # Remove the plugin menu item and icon
            for action in self.actions:
                self.iface.removePluginMenu(PaddockPower.MENU_NAME, action)
                self.iface.removeToolBarIcon(action)

            # Remove the toolbar
            del self.toolbar
        except BaseException:
            pass

        try:
            self.unloadWorkspace()
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

    # @Glitch.glitchy(f"An error occurred while scanning for {PLUGIN_NAME} workspaces.")
    def detectWorkspace(self, warning=False):
        f"""Detect a {PLUGIN_NAME} workspace adjacent to the current QGIS project."""

        self.unloadWorkspace()

        projectFile = resolveProjectFile()
        if projectFile is None:
            qgsInfo(f"{PLUGIN_NAME} no QGIS project file located …")
            if warning:
                guiError(
                    f"Please create and save a QGIS project file before you try to detect a {PLUGIN_NAME} workspace.")
            return
        else:
            workspaceFile = resolveWorkspaceFile()
            if workspaceFile and os.path.exists(workspaceFile):
                self.workspace = self.container.workspace()
            else:
                qgsInfo(f"{PLUGIN_NAME} no workspace (.gpkg) file was located …")

    # @Glitch.glitchy(f"An error occurred while creating a {PLUGIN_NAME} workspace.")
    def createWorkspace(self):
        f"""Create a new {PLUGIN_NAME} workspace in the current QGIS project."""
        # try:
        projectFile = resolveProjectFile()
        if projectFile is None:
            qgsInfo(f"{PLUGIN_NAME} no QGIS project file located …")
            # guiError(f"Please create and save a QGIS project file before you try to create a {PLUGIN_NAME} workspace.")
            return
        else:
            workspaceFile = resolveWorkspaceFile()
            if workspaceFile is not None:
                if os.path.exists(workspaceFile):
                    qgsInfo(f"A {PLUGIN_NAME} workspace (.gpkg) file already exists. Stopping creation …")
                    # guiError(f"A {PLUGIN_NAME} workspace file {os.path.basename(workspaceFile)} already exists alongside your QGIS project file.")
                else:
                    self.workspace = self.container.workspace()
                    qgsInfo(f"{PLUGIN_NAME} created workspace …")
                    # guiInformation(f"A new {PLUGIN_NAME} workspace file, {os.path.basename(workspaceFile)} has been created alongside your QGIS project file.")
            else:
                qgsInfo(f"{PLUGIN_NAME} no workspace (.gpkg) file was located …")
        # except BaseException as e:
        #     qgsInfo(f"{PLUGIN_NAME} exception occurred creating workspace …")
        #     qgsException()
        #     raise e
        #     pass

    def importData(self):
        if self.workspace is not None:
            self.workspace.importData()

    def resetWorkspace(self):
        # Prime the container for a new workspace
        if self.container:
            self.container.reset_singletons()

    def unloadWorkspace(self):
        """Removes the plugin menu item and icon from QGIS interface."""
        if self.workspace is not None:
            qgsInfo(f"{PLUGIN_NAME} unloading workspace …")
            self.workspace.unload()
            self.workspace = None

        # Reset the DI container
        self.container.reset_singletons()

    def openFeatureView(self):
        if self.workspace is not None:
            self.workspace.openFeatureView()
