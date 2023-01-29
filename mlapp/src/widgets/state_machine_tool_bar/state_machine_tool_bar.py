# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QToolBar

from ...utils import getComponentStyleSheet


STYLESHEET = getComponentStyleSheet(__file__)


class StateToolBarAction(QAction):
    def __init__(self, stateAction, icon, text, callback, parent=None):
        super().__init__(icon, text, parent)

        self.stateAction = stateAction
        self.triggered.connect(callback)


class GenericToolBarAction(QAction):
    def __init__(self, icon, text, callback, parent=None):
        super().__init__(icon, text, parent)
        self.triggered.connect(callback)


class StateMachineToolBar(QToolBar):
    layoutRefreshNeeded = pyqtSignal()

    def __init__(self, machine, parent=None):
        super().__init__(parent)

        self._showStateActions = True

        self.machine = machine

        self.stateActions = []
        self.genericActions = []

        self.setStyleSheet(STYLESHEET)
        self.setFixedHeight(30)

        self.machine.statusChanged = self.refreshUi
        self.refreshUi()

    def addStateAction(self, stateAction, icon, callback):
        """Add a feature action to the toolbar."""
        text = f"{stateAction} {self.machine.displayName()}"
        action = StateToolBarAction(stateAction, QIcon(icon), text, callback, self)
        self.stateActions.append(action)

    def addGenericAction(self, icon, text, callback):
        action = GenericToolBarAction(QIcon(icon), text, callback, self)
        self.genericActions.append(action)
        self.refreshUi()

    def hideStateActions(self):
        self._showStateActions = False
        self.refreshUi()

    def refreshUi(self):
        """Refresh the UI based on the current state of the fence."""

        self.clear()

        permitted = self.machine.allPermitted()
        permittedStateActions = [a for a in self.stateActions if a.stateAction.match(*permitted)]

        if self._showStateActions:
            for action in permittedStateActions:
                self.addAction(action)

        for action in self.genericActions:
            self.addAction(action)

        self.layoutRefreshNeeded.emit()
