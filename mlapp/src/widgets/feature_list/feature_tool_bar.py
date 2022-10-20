# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QSize, pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QHBoxLayout, QSizePolicy, QToolBar

from ...models.state import State


class FeatureToolBar(QToolBar):
    layoutRefreshNeeded = pyqtSignal()

    # Editing signals
    plan = pyqtSignal()
    undoPlan = pyqtSignal()

    def __init__(self, feature, parent=None):
        super().__init__(parent)

        self.state = State()

        self.feature = feature
        self.featureActions = {}

        self.setStyleSheet("""QToolBar { padding: 0; }
                                      QToolButton::indicator {
                                        height: 20;
                                        width: 20;
                                      }""")
        self.setFixedHeight(30)
        
        self.feature.stateChanged.connect(self.refreshUi)

        self.refreshUi()

    def addFeatureAction(self, action, icon, callback):
        """Add a feature action to the toolbar."""
        featureAction = QAction(QIcon(icon), f"{action} {self.feature.featureTypeDisplayName()}", self)
        featureAction.triggered.connect(callback)
        self.featureActions[action] = featureAction
        self.addAction(featureAction)

    def addZoomAction(self):
        self.zoomAction = QAction(QIcon(
            ':/plugins/mlapp/images/paddock-zoom.png'), self.tr(u'Zoom to Fence'), self)

        self.zoomAction.triggered.connect(self.selectFeature)
        self.addAction(self.zoomAction)

   
    def refreshUi(self):
        """Refresh the UI based on the current state of the fence."""

        permitted = self.feature.allPermitted()

        # Hide or show Feature actions
        for (action, featureAction) in self.featureActions.items():
            featureAction.setVisible(action in permitted)

        # Force a layout refresh
        self.layoutRefreshNeeded.emit()

    def selectFeature(self):
        """Select this Feature."""
        milestone = self.state.getMilestone()
        if milestone is not None:
            milestone.setSelectedFeature(self.feature)

    def zoomToFeature(self, title):
        """Select this Fence and zoom to it."""
        self.selectFeature()
        self.feature.zoomToFeature()

  