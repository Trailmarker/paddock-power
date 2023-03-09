# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QButtonGroup, QDockWidget, QToolBar

from qgis.core import QgsProject

from ...models import WorkspaceMixin
from ...utils import getComponentStyleSheet, qgsInfo, PLUGIN_FOLDER, PLUGIN_NAME
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

        self._pluginInitGui = False
        self._uiBuilt = False

        self.setupUi(self)
        self.setStyleSheet(STYLESHEET)

        self.paddockTab = None
        self.fenceTab = None
        self.pipelineTab = None
        self.waterpointTab = None

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

        # Create a button group to control checking of the Timeframe buttons
        self.timeframeButtonGroup = QButtonGroup(exclusive=True)
        self.timeframeButtonGroup.addButton(self.currentTimeframeButton)
        self.timeframeButtonGroup.addButton(self.futureTimeframeButton)

    def initGui(self):
        f"""Called when the {PLUGIN_NAME} plugin calls initGui()."""
        if not self._pluginInitGui:
            self.plugin.workspaceUnloading.connect(self.clearUi)
            self.plugin.workspaceReady.connect(self.buildUi)
            self._pluginInitGui = True

    def refreshUi(self):
        self.paddockTab.refreshUi()

        if self.workspace:
            self.currentTimeframeButton.setChecked(self.workspace.timeframe.name == 'Current')
            self.futureTimeframeButton.setChecked(self.workspace.timeframe.name == 'Future')

    def buildUi(self):
        if self._uiBuilt:
            qgsInfo(f"{PLUGIN_NAME} already built?")

        qgsInfo(f"{PLUGIN_NAME} rebuilding feature view …")

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

        self.currentTimeframeButton.clicked.connect(lambda: self.workspace.setTimeframe("Current"))
        self.futureTimeframeButton.clicked.connect(lambda: self.workspace.setTimeframe("Future"))

        self.sketchFenceButton.clicked.connect(self.fenceTab.sketchFence)
        self.sketchPipelineButton.clicked.connect(self.pipelineTab.sketchPipeline)
        self.sketchWaterpointButton.clicked.connect(self.waterpointTab.sketchWaterpoint)

        self.workspace.timeframeChanged.connect(lambda _: self.refreshUi())
        self.workspace.featureLayerSelected.connect(lambda layerId: self.onFeatureLayerSelected(layerId))

        self._uiBuilt = True
        qgsInfo(f"{PLUGIN_NAME} rebuilt.")

    def clearUi(self):
        if not self._uiBuilt:
            return

        qgsInfo(f"{PLUGIN_NAME} tearing down old feature view …")

        while (self.tabWidget.count() > 0):
            self.tabWidget.removeTab(0)

        self.paddockTab = None
        self.fenceTab = None
        self.pipelineTab = None
        self.waterpointTab = None

        for item in [
            self.currentTimeframeButton, self.futureTimeframeButton,
            self.sketchFenceButton,
            self.sketchPipelineButton,
            self.sketchWaterpointButton
        ]:
            try:
                item.clicked.disconnect()
            except BaseException:
                pass
        self.timeframeButtonGroup = None
        self._uiBuilt = False
        qgsInfo(f"{PLUGIN_NAME} torn down.")

        # self.update()

    def onFeatureLayerSelected(self, layerId):
        featureLayer = QgsProject.instance().mapLayer(layerId)
        name = featureLayer.getFeatureType().__name__
        if name == 'FenceLayer':
            self.tabWidget.setCurrentWidget(self.fenceTab)
        elif name == 'PaddockLayer':
            self.tabWidget.setCurrentWidget(self.paddockTab)
        elif name == 'PipelineLayer':
            self.tabWidget.setCurrentWidget(self.pipelineTab)
        if name == 'WaterpointLayer':
            self.tabWidget.setCurrentWidget(self.waterpointTab)
