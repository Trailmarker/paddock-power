# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QToolBar

from ...models.state import State
from ...utils import qgsDebug


class FeatureToolBarAction(QAction):
    def __init__(self, featureAction, icon, text, callback, parent=None):
        super().__init__(icon, text, parent)

        self.featureAction = featureAction
        self.triggered.connect(callback)


class FeatureToolBar(QToolBar):
    layoutRefreshNeeded = pyqtSignal()

    def __init__(self, feature, parent=None):
        super().__init__(parent)

        self.state = State()

        self.feature = feature
        self.zoomAction = False
        self.featureActions = []

        self.setStyleSheet("""QToolBar { padding: 0; }
                                      QToolButton::indicator {
                                        height: 20;
                                        width: 20;
                                      }""")
        self.setFixedHeight(30)

        self.feature.stateChanged.connect(self.refreshUi)

        self.refreshUi()

    def addFeatureAction(self, featureAction, icon, callback):
        """Add a feature action to the toolbar."""
        text = f"{featureAction} {self.feature.displayName()}"
        action = FeatureToolBarAction(featureAction, QIcon(icon), text, callback, self)
        self.featureActions.append(action)

    def addZoomAction(self):
        self.zoomAction = True
   
    def refreshUi(self):
        """Refresh the UI based on the current state of the fence."""

        self.clear()

        permitted = self.feature.allPermitted()

        permittedFeatureActions = [a for a in self.featureActions if a.featureAction.match(*permitted)]

        for action in permittedFeatureActions:
            self.addAction(action)

        if self.zoomAction:
            self.zoomAction = QAction(QIcon(
                ':/plugins/mlapp/images/paddock-zoom.png'), f"Zoom to {self.feature.displayName()}", self)
            self.zoomAction.triggered.connect(self.selectFeature)
            self.addAction(self.zoomAction)

        # Force a layout refresh
        self.layoutRefreshNeeded.emit()

    def selectFeature(self):
        """Select this Feature."""
        project = self.state.getProject()
        if project is not None:
            project.setSelectedFeature(self.feature)

    def zoomToFeature(self, title):
        """Select this Fence and zoom to it."""
        self.selectFeature()
        self.feature.zoomToFeature()
