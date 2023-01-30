# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QButtonGroup, QDockWidget, QToolBar

from ...spatial.fields.timeframe import Timeframe
from ...models.workspace_mixin import WorkspaceMixin
from ...utils import getComponentStyleSheet, PLUGIN_FOLDER
from ..fence_widget import FenceWidget
from ..paddock_widget import PaddockWidget
from ..pipeline_widget import PipelineWidget
from ..waterpoint_widget import WaterpointWidget

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'feature_view_base.ui')))

STYLESHEET = getComponentStyleSheet(__file__)


class FeatureView(QDockWidget, FORM_CLASS, WorkspaceMixin):

    closingView = pyqtSignal(type)

    def __init__(self, parent=None):
        """Constructor."""
        QDockWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)
        WorkspaceMixin.__init__(self)

        self.setupUi(self)

        self.setStyleSheet(STYLESHEET)

        self.paddockTab = PaddockWidget(self.tabWidget)
        self.fenceTab = FenceWidget(self.tabWidget)
        self.pipelineTab = PipelineWidget(self.tabWidget)
        self.waterpointTab = WaterpointWidget(self.tabWidget)

        self.tabWidget.addTab(self.paddockTab, QIcon(f":/plugins/{PLUGIN_FOLDER}/images/paddock.png"), 'Paddocks')
        self.tabWidget.addTab(self.fenceTab, QIcon(f":/plugins/{PLUGIN_FOLDER}/images/fence.png"), 'Fences')
        self.tabWidget.addTab(
            self.pipelineTab,
            QIcon(f":/plugins/{PLUGIN_FOLDER}/images/pipeline-dashed.png"),
            'Pipelines')
        self.tabWidget.addTab(
            self.waterpointTab,
            QIcon(f":/plugins/{PLUGIN_FOLDER}/images/waterpoint.png"),
            'Waterpoints')

        self.currentTimeframeButton.clicked.connect(lambda: self.workspace.setTimeframe(Timeframe.Current))
        self.futureTimeframeButton.clicked.connect(lambda: self.workspace.setTimeframe(Timeframe.Future))

        # Create a button group to control checking of the Timeframe buttons
        self.timeframeButtonGroup = QButtonGroup(exclusive=True)
        self.timeframeButtonGroup.addButton(self.currentTimeframeButton)
        self.timeframeButtonGroup.addButton(self.futureTimeframeButton)

        self.sketchFenceButton.clicked.connect(self.fenceTab.sketchFence)
        self.sketchPipelineButton.clicked.connect(self.pipelineTab.sketchPipeline)
        self.sketchWaterpointButton.clicked.connect(self.waterpointTab.sketchWaterpoint)

        self.toolBar = QToolBar()
        self.toolBar.setMovable(False)
        self.toolBar.setFloatable(False)
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolBar.addWidget(self.currentTimeframeButton)
        self.toolBar.addWidget(self.futureTimeframeButton)
        self.toolBar.addWidget(self.sketchFenceButton)
        self.toolBar.addWidget(self.sketchPipelineButton)
        self.toolBar.addWidget(self.sketchWaterpointButton)

        self.tabWidget.setCornerWidget(self.toolBar)
        self.workspace.timeframeChanged.connect(lambda _: self.refreshUi())

        self.refreshUi()

      

    def refreshUi(self):
        if self.ready:
            self.currentTimeframeButton.setChecked(self.workspace.timeframe == Timeframe.Current)
            self.futureTimeframeButton.setChecked(self.workspace.timeframe == Timeframe.Future)
