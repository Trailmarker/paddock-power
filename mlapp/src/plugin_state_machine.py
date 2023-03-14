# -*- coding: utf-8 -*-
from functools import partial

from qgis.PyQt.QtCore import QObject, pyqtSignal

from .models import QtAbstractMeta, StateMachineAction, StateMachine, StateMachineStatus, actionHandlerWithException


class PluginActionFailure(Exception):
    pass


class PluginAction(StateMachineAction):
    def handler(self):
        return partial(actionHandlerWithException, self, PluginActionFailure)

    """Allowed transitions for a StatusFeature."""
    detectWorkspace = "Detect Workspace"
    createWorkspace = "Create Workspace"
    loadWorkspace = "Load Workspace"
    refreshWorkspace = "Refresh Workspace"
    analyseWorkspace = "Analyse Workspace"
    openPluginDockWidget = "Open Plugin Dock Widget"
    closePluginDockWidget = "Close Plugin Dock Widget"
    openImportDialog = "Import Data"
    unloadWorkspace = "Unload Workspace"
    projectClosed = "Project Closed"


class PluginStatus(StateMachineStatus):
    """Allowed statuses for a StatusFeature."""
    NoProjectOpen = "No Project Open"
    NoWorkspaceLoaded = "No Workspace Loaded"
    WorkspaceLoaded = "Workspace Loaded"


class PluginStateMachine(QObject, StateMachine, metaclass=QtAbstractMeta):

    _stateChanged = pyqtSignal()

    def __init__(self, status=PluginStatus.NoWorkspaceLoaded):
        QObject.__init__(self)
        StateMachine.__init__(self)

        self._status = status

    # State machine interface
    __TRANSITIONS = {

        (PluginStatus.NoWorkspaceLoaded, PluginAction.createWorkspace): PluginStatus.NoWorkspaceLoaded,
        (PluginStatus.NoWorkspaceLoaded, PluginAction.detectWorkspace): PluginStatus.NoWorkspaceLoaded,
        (PluginStatus.NoWorkspaceLoaded, PluginAction.loadWorkspace): PluginStatus.WorkspaceLoaded,
        (PluginStatus.NoWorkspaceLoaded, PluginAction.projectClosed): PluginStatus.NoWorkspaceLoaded,

        (PluginStatus.WorkspaceLoaded, PluginAction.refreshWorkspace): PluginStatus.WorkspaceLoaded,
        (PluginStatus.WorkspaceLoaded, PluginAction.analyseWorkspace): PluginStatus.WorkspaceLoaded,
        (PluginStatus.WorkspaceLoaded, PluginAction.openPluginDockWidget): PluginStatus.WorkspaceLoaded,
        (PluginStatus.WorkspaceLoaded, PluginAction.closePluginDockWidget): PluginStatus.WorkspaceLoaded,
        (PluginStatus.WorkspaceLoaded, PluginAction.openImportDialog): PluginStatus.WorkspaceLoaded,
        (PluginStatus.WorkspaceLoaded, PluginAction.unloadWorkspace): PluginStatus.NoWorkspaceLoaded,
        (PluginStatus.WorkspaceLoaded, PluginAction.projectClosed): PluginStatus.NoWorkspaceLoaded
    }

    @property
    def transitions(self):
        return PluginStateMachine.__TRANSITIONS

    @property
    def actionType(self):
        return PluginAction

    @property
    def statusType(self):
        return PluginStatus

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, stat):
        self._status = stat

    def displayName(self):
        return self._status.value

    @property
    def stateChanged(self):
        return self._stateChanged

    def emitStateChanged(self):
        self.stateChanged.emit()
