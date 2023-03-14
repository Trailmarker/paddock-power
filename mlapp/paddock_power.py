# -*- coding: utf-8 -*-
import os.path
import sys
import traceback

from qgis.PyQt.QtCore import Qt, QCoreApplication, QSettings, QTranslator, pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from qgis.core import QgsExpression, QgsProject

from .resources_rc import *

from .src.models import Glitch, Workspace
from .src.paddock_power_functions import PaddockPowerFunctions
from .src.plugin_state_machine import PluginStateMachine, PluginAction, PluginActionFailure, PluginStatus
from .src.utils import guiConfirm, guiStatusBar, guiStatusBarAndInfo, guiWarning, qgsDebug, qgsException, qgsInfo, resolveWorkspaceFile, resolveProjectFile, PLUGIN_FOLDER, PLUGIN_NAME
from .src.widgets.plugin_dock_widget import PluginDockWidget
from .src.widgets.dialogs.import_dialog import ImportDialog


class PaddockPower(PluginStateMachine):

    MENU_NAME = f"&{PLUGIN_NAME}"

    __GLITCH_HOOK_WRAPPER = "__glitchHookWrapper"

    caughtGlitch = pyqtSignal(Glitch)

    def __init__(self, iface):
        super().__init__()

        self.status = PluginStatus.NoWorkspaceLoaded
        self.workspace = None

        self.iface = iface
        self.actions = {}

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

        QgsProject.instance().cleared.connect(self.projectClosed)
        QgsProject.instance().readProject.connect(self.detectWorkspace)

        self.pluginDockWidget = PluginDockWidget(self.iface.mainWindow())
        self.pluginDockWidget.setVisible(False)
        self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.pluginDockWidget)

    def addAction(self,
                  pluginAction,
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
        self.actions[pluginAction] = action
        return action

    def initGui(self):
        """The real Paddock Power GUI is initialised when a QGIS project is opened,
           but QGIS utilities call this when the plug-in is loaded anyway."""

        # Initialise plug-in menu and toolbar
        self.menu = PaddockPower.MENU_NAME

        self.toolbar = self.iface.addToolBar(u"PaddockPower")
        self.toolbar.setObjectName(u"PaddockPower")

        self.openPluginDockWidgetAction = self.addAction(PluginAction.openPluginDockWidget,
                                                    QIcon(f":/plugins/{PLUGIN_FOLDER}/images/paddock-power.png"),
                                                    text=f"Open {PLUGIN_NAME} …",
                                                    callback=lambda *_: self.openPluginDockWidget(),
                                                    parent=self.iface.mainWindow())

        self.detectWorkspaceAction = self.addAction(
            PluginAction.detectWorkspace,
            QIcon(f":/plugins/{PLUGIN_FOLDER}/images/refresh-paddock-power.png"),
            text=f"Detect {PLUGIN_NAME} workspace …",
            callback=lambda *_: self.detectWorkspace(),
            parent=self.iface.mainWindow())

        self.refreshWorkspaceAction = self.addAction(
            PluginAction.refreshWorkspace,
            QIcon(f":/plugins/{PLUGIN_FOLDER}/images/refresh-paddock-power.png"),
            text=f"Refresh {PLUGIN_NAME} workspace …",
            callback=lambda *_: self.refreshWorkspace(),
            parent=self.iface.mainWindow())

        self.analyseWorkspaceAction = self.addAction(
            PluginAction.analyseWorkspace,
            QIcon(f":/plugins/{PLUGIN_FOLDER}/images/analyse-paddock-power.png"),
            text=f"Analyse {PLUGIN_NAME} workspace …",
            callback=lambda *_: self.analyseWorkspace(),
            parent=self.iface.mainWindow())

        self.createWorkspaceAction = self.addAction(
            PluginAction.createWorkspace,
            QIcon(f":/plugins/{PLUGIN_FOLDER}/images/new-paddock-power.png"),
            text=f"Create {PLUGIN_NAME} workspace …",
            callback=lambda *_: self.createWorkspace(),
            parent=self.iface.mainWindow())

        self.importDataAction = self.addAction(
            PluginAction.openImportDialog,
            QIcon(f":/plugins/{PLUGIN_FOLDER}/images/import.png"),
            text=f"Import {PLUGIN_NAME} Data …",
            callback=lambda *_: self.openImportDialog(),
            parent=self.iface.mainWindow())

        self._stateChanged.connect(self.refreshUi)

        if self.status == PluginStatus.NoWorkspaceLoaded:
            self.detectWorkspace(False)

    def setupGlitchHook(self):
        """Set up a global exception hook to catch Glitch exceptions and process them."""
        if hasattr(sys.excepthook, PaddockPower.__GLITCH_HOOK_WRAPPER):
            qgsInfo("GlitchHook: Glitch hook already set.")
            return

        exceptHook = sys.excepthook
        qgsInfo("GlitchHook: setting up Glitch hook.")

        def glitchHookWrapper(exceptionType, e, tb):
            if isinstance(e, Glitch):
                qgsDebug(f"Caught Glitch: {e}")
                qgsDebug(traceback.format_exception(exceptionType, e, tb))
                self.caughtGlitch.emit(e)
                return
            else:
                exceptHook(exceptionType, e, tb)

        setattr(glitchHookWrapper, PaddockPower.__GLITCH_HOOK_WRAPPER, sys.excepthook)
        sys.excepthook = glitchHookWrapper

    @staticmethod
    def restoreSystemExceptionHook():
        if hasattr(sys.excepthook, PaddockPower.__GLITCH_HOOK_WRAPPER):
            qgsInfo("GlitchHook: restoring original system exception hook.")
            sys.excepthook = getattr(sys.excepthook, PaddockPower.__GLITCH_HOOK_WRAPPER)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS interface."""
        qgsInfo(f"Unloading {PLUGIN_NAME} plugin …")
        try:
            QgsProject.instance().cleared.disconnect(self.projectClosed)
            QgsProject.instance().readProject.disconnect(self.detectWorkspace)
            qgsInfo(f"Signals disconnected …")

        except BaseException:
            qgsException()
        try:
            self.pluginDockWidget.clearUi()
            self.pluginDockWidget.setVisible(False)
            self.pluginDockWidget.setParent(None)
            self.iface.removeDockWidget(self.pluginDockWidget)
            self.pluginDockWidget.deleteLater()
            self.pluginDockWidget = None
            qgsInfo(f"Dock widget destroyed …")
        except BaseException:
            qgsException()
        try:
            self.unloadWorkspace()
            qgsInfo(f"Workspace unloaded …")
        except BaseException:
            qgsException()
        try:
            # Remove the plugin menu item and icon
            for action in self.actions:
                self.iface.removePluginMenu(PaddockPower.MENU_NAME, self.actions[action])
                self.iface.removeToolBarIcon(self.actions[action])

            # Remove the toolbar
            del self.toolbar
            qgsInfo(f"Toolbar and actions removed …")
        except BaseException:
            qgsException()
        try:
            # Unregister the extension functions
            self.unregisterFunctions()
            qgsInfo(f"Expression functions unregistered …")
        except BaseException:
            qgsException()

        PaddockPower.restoreSystemExceptionHook()
        qgsInfo(f"{PLUGIN_NAME} unloaded.")

    def registerFunctions(self):
        f"""Register the extension functions used by {PLUGIN_NAME}."""
        for paddockPowerFunction in PaddockPowerFunctions:
            QgsExpression.registerFunction(PaddockPowerFunctions[paddockPowerFunction])

    def unregisterFunctions(self):
        f"""Register the extension functions used by {PLUGIN_NAME}."""
        for paddockPowerFunction in PaddockPowerFunctions:
            QgsExpression.unregisterFunction(paddockPowerFunction)

    def initWorkspace(self, workspaceFile):
        if self.workspace:
            self.unloadWorkspace()
        workspace = Workspace(self.iface, workspaceFile)
        workspace.workspaceLoaded.connect(lambda: self.onWorkspaceLoaded(workspace))

    @PluginAction.loadWorkspace.handler()
    def onWorkspaceLoaded(self, workspace):
        guiStatusBarAndInfo(f"{PLUGIN_NAME} workspace loaded: {workspace.workspaceName}")
        self.workspace = workspace
        self.pluginDockWidget.buildUi()

    def detectWorkspace(self, warning=True):
        f"""Detect a {PLUGIN_NAME} workspace adjacent to the current QGIS project."""

        try:
            projectFile = resolveProjectFile()
            if projectFile is None:
                if warning:
                    self.__failureMessage(f"No {PLUGIN_NAME} workspace (.gpkg) file was located …")
                return
            else:
                workspaceFile = resolveWorkspaceFile(projectFilePath=projectFile)
                if workspaceFile and os.path.exists(workspaceFile):
                    self.initWorkspace(workspaceFile)
                else:
                    if warning:
                        self.__failureMessage(f"No {PLUGIN_NAME} workspace (.gpkg) file was located …")
                    return
        except BaseException:
            qgsInfo(f"{PLUGIN_NAME} exception occurred detecting workspace …")
            qgsException()
            self.__failureMessage(
                f"An unexpected error occurred creating your {PLUGIN_NAME} workspace. Please check the QGIS logs for details …")

    def refreshWorkspace(self):
        f"""Refresh the {PLUGIN_NAME} workspace."""
        if self.status == PluginStatus.WorkspaceLoaded:
            self.doAction(PluginAction.unloadWorkspace)
        self.detectWorkspace()

    def createWorkspace(self):
        f"""Create a new {PLUGIN_NAME} workspace in the current QGIS project."""

        try:
            projectFile = resolveProjectFile()
            if projectFile is None:
                self.__failureMessage(f"{PLUGIN_NAME} no QGIS project file located …")
                return
            else:
                workspaceFile = resolveWorkspaceFile()
                if workspaceFile is not None:
                    if os.path.exists(workspaceFile):
                        self.__failureMessage(
                            f"A {PLUGIN_NAME} workspace (.gpkg) file already exists. Stopping creation …")
                        return
                    else:
                        self.initWorkspace(workspaceFile)
                else:
                    qgsInfo(f"No workspace {PLUGIN_NAME} (.gpkg) file was located …")
        except BaseException:
            qgsInfo(f"{PLUGIN_NAME} exception occurred creating workspace …")
            qgsException()
            self.__failureMessage(
                f"An unexpected error occurred creating your {PLUGIN_NAME} workspace. Please check the QGIS logs for details …")

    @PluginAction.analyseWorkspace.handler()
    def analyseWorkspace(self):
        """Recalculates then re-derives the whole workspace."""

        if guiConfirm(
            f"This will analyse or re-derive all {PLUGIN_NAME} workspace measurements, including property feature elevations, lengths, and areas, as well as derived paddock metrics.",
                f"Analyse {PLUGIN_NAME} workspace?"):
            self.workspace.analyseWorkspace()

    @PluginAction.projectClosed.handler()
    def projectClosed(self):
        projectFile = resolveProjectFile()

        if not projectFile:
            self.pluginDockWidget.setVisible(False)
            self.unloadWorkspace()

    def unloadWorkspace(self):
        f"""Unloads the {PLUGIN_NAME} workspace."""
        if self.workspace is not None:
            qgsInfo(f"{PLUGIN_NAME} unloading workspace …")
            if self.pluginDockWidget:
                self.pluginDockWidget.clearUi()
            self.workspace.unload()
            self.workspace = None

    @PluginAction.openPluginDockWidget.handler()
    def openPluginDockWidget(self):
        self.pluginDockWidget.setVisible(True)

    @PluginAction.closePluginDockWidget.handler()
    def closePluginDockWidget(self):
        self.pluginDockWidget.setVisible(False)

    @PluginAction.openImportDialog.handler()
    def openImportDialog(self):
        if self.workspace:
            self.importDialog = ImportDialog(self, self.iface.mainWindow())
            self.importDialog.show()
        else:
            self.__failureMessage(f"{PLUGIN_NAME} no workspace loaded …")
            raise PluginActionFailure()

    def __successMessage(self, message):
        guiStatusBar(message)

    def __failureMessage(self, message):
        guiWarning(message)

    def refreshUi(self):
        for pluginAction in self.actions:
            if self.isPermitted(pluginAction):
                self.actions[pluginAction].setEnabled(True)
            else:
                self.actions[pluginAction].setEnabled(False)
