# -*- coding: utf-8 -*-
import os.path
import sys

from qgis.PyQt.QtCore import Qt, QCoreApplication, QSettings, QTranslator, pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from qgis.core import QgsExpression, QgsProject

from .resources_rc import *

from .src.models import Glitch, Workspace
from .src.paddock_power_functions import PaddockPowerFunctions
from .src.plugin_state_machine import PluginStateMachine, PluginAction, PluginActionFailure, PluginStatus
from .src.utils import guiStatusBar, guiWarning, qgsException, qgsInfo, resolveWorkspaceFile, resolveProjectFile, PLUGIN_FOLDER, PLUGIN_NAME
from .src.views.feature_view.feature_view import FeatureView
from .src.widgets.import_dialog.import_dialog import ImportDialog


class PaddockPower(PluginStateMachine):

    MENU_NAME = f"&{PLUGIN_NAME}"

    __GLITCH_HOOK_WRAPPER = "__glitchHookWrapper"

    caughtGlitch = pyqtSignal(Glitch)
    workspaceReady = pyqtSignal()
    workspaceUnloading = pyqtSignal()
    triggerDetectWorkspace = pyqtSignal()

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

        self.featureView = FeatureView(self.iface.mainWindow())
        self.featureView.setVisible(False)
        self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.featureView)

        self._stateChanged.connect(self.refreshUi)
        self.triggerDetectWorkspace.connect(lambda: self.detectWorkspace(warning=False))

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

        self.openFeatureViewAction = self.addAction(PluginAction.openFeatureView,
                                                    QIcon(f":/plugins/{PLUGIN_FOLDER}/images/paddock-power.png"),
                                                    text=f"Open {PLUGIN_NAME} …",
                                                    callback=lambda *_: self.openFeatureView(),
                                                    parent=self.iface.mainWindow())

        self.detectWorkspaceAction = self.addAction(
            PluginAction.detectWorkspace,
            QIcon(f":/plugins/{PLUGIN_FOLDER}/images/refresh-paddock-power.png"),
            text=f"Refresh {PLUGIN_NAME} workspace …",
            callback=lambda *_: self.detectWorkspace(),
            parent=self.iface.mainWindow())

        self.analyseWorkspaceAction = self.addAction(
            PluginAction.analyseWorkspace,
            QIcon(f":/plugins/{PLUGIN_FOLDER}/images/refresh-paddock-power.png"),
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

        self.featureView.initGui()
        self.refreshUi()

        if self.status == PluginStatus.NoWorkspaceLoaded:
            self.triggerDetectWorkspace.emit()

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
        qgsInfo(f"Unloading {PLUGIN_NAME} plugin …")
        try:
            QgsProject.instance().cleared.disconnect(self.projectClosed)
            QgsProject.instance().readProject.disconnect(self.detectWorkspace)
            qgsInfo(f"Signals disconnected …")

        except BaseException:
            qgsException()
        try:
            self.featureView.clearUi()
            self.featureView.setVisible(False)
            self.featureView.setParent(None)
            self.iface.removeDockWidget(self.featureView)
            self.featureView.deleteLater()
            self.featureView = None
            qgsInfo(f"Feature View destroyed …")
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
            self.workspaceUnloading.emit()
        self.workspace = Workspace(self.iface, workspaceFile)
        qgsInfo("Emitting workspaceReady …")
        self.workspaceReady.emit()

    @PluginAction.detectWorkspace.handler()
    def detectWorkspace(self, warning=True):
        f"""Detect a {PLUGIN_NAME} workspace adjacent to the current QGIS project."""

        try:
            projectFile = resolveProjectFile()
            if projectFile is None:
                if warning:
                    self.__failureMessage(f"No {PLUGIN_NAME} workspace (.gpkg) file was located …")
                raise PluginActionFailure()
            else:
                workspaceFile = resolveWorkspaceFile(projectFilePath=projectFile)
                if workspaceFile and os.path.exists(workspaceFile):
                    self.initWorkspace(workspaceFile)
                    self.__successMessage(
                        f"{PLUGIN_NAME} loaded workspace (.gpkg) from {os.path.split(os.path.basename(workspaceFile))[1]}.")
                else:
                    if warning:
                        self.__failureMessage(f"No {PLUGIN_NAME} workspace (.gpkg) file was located …")
                    raise PluginActionFailure()
        except PluginActionFailure as e:
            raise e
        except BaseException:
            qgsInfo(f"{PLUGIN_NAME} exception occurred detecting workspace …")
            qgsException()
            self.__failureMessage(
                f"An unexpected error occurred creating your {PLUGIN_NAME} workspace. Please check the QGIS logs for details …")

    @PluginAction.createWorkspace.handler()
    def createWorkspace(self):
        f"""Create a new {PLUGIN_NAME} workspace in the current QGIS project."""

        try:
            projectFile = resolveProjectFile()
            if projectFile is None:
                self.__failureMessage(f"{PLUGIN_NAME} no QGIS project file located …")
                raise PluginActionFailure()
            else:
                workspaceFile = resolveWorkspaceFile()
                if workspaceFile is not None:
                    if os.path.exists(workspaceFile):
                        self.__failureMessage(
                            f"A {PLUGIN_NAME} workspace (.gpkg) file already exists. Stopping creation …")
                        raise PluginActionFailure()
                    else:
                        self.initWorkspace(workspaceFile)
                        qgsInfo(f"{PLUGIN_NAME} created workspace …")
                        self.__successMessage(
                            f"A new {PLUGIN_NAME} workspace file, {os.path.split(os.path.basename(workspaceFile))[1]} has been created alongside your QGIS project file.")
                else:
                    qgsInfo(f"No workspace {PLUGIN_NAME} (.gpkg) file was located …")
        except PluginActionFailure as e:
            raise e
        except BaseException:
            qgsInfo(f"{PLUGIN_NAME} exception occurred creating workspace …")
            qgsException()
            self.__failureMessage(
                f"An unexpected error occurred creating your {PLUGIN_NAME} workspace. Please check the QGIS logs for details …")

    @PluginAction.analyseWorkspace.handler()
    def analyseWorkspace(self):
        self.workspace.recalculateLayers()

    @PluginAction.projectClosed.handler()
    def projectClosed(self):
        projectFile = resolveProjectFile()

        if not projectFile:
            self.featureView.setVisible(False)
            self.unloadWorkspace()

    def unloadWorkspace(self):
        f"""Unloads the {PLUGIN_NAME} workspace."""
        if self.workspace is not None:
            self.workspaceUnloading.emit()
            qgsInfo(f"{PLUGIN_NAME} unloading workspace …")
            self.workspace.unload()
            self.workspace = None

    @PluginAction.openFeatureView.handler()
    def openFeatureView(self):
        self.featureView.setVisible(True)

    @PluginAction.closeFeatureView.handler()
    def closeFeatureView(self):
        self.featureView.setVisible(False)

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
