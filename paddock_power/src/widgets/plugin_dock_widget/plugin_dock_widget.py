# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QButtonGroup, QDockWidget, QToolBar, QPushButton

from ...layers.fields import Timeframe
from ...models import WorkspaceMixin
from ...pdf_report.pdf_report_dialog import PdfReportDialog
from ...utils import getComponentStyleSheet, qgsInfo, PLUGIN_FOLDER, PLUGIN_NAME
from .fences_widget import FencesWidget
from .land_types_widget import LandTypesWidget
from .paddocks_widget import PaddocksWidget
from .pipelines_widget import PipelinesWidget
from .waterpoints_widget import WaterpointsWidget

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'plugin_dock_widget_base.ui')))

STYLESHEET = getComponentStyleSheet(__file__)


class PluginDockWidget(QDockWidget, FORM_CLASS, WorkspaceMixin):

    closingView = pyqtSignal(type)

    def __init__(self, parent=None):
        """Constructor."""
        QDockWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)
        WorkspaceMixin.__init__(self)

        self._uiBuilt = False

        self.setupUi(self)
        self.setStyleSheet(STYLESHEET)

        self.paddocksWidget = None
        self.landTypesWidget = None
        self.fencesWidget = None
        self.pipelinesWidget = None
        self.waterpointsWidget = None

        self.pdfReportDialog = None
        self.pdfReportButton = QPushButton(QIcon(f":/plugins/{PLUGIN_FOLDER}/images/pdf-icon.png"), '', self)
        self.pdfReportButton.setToolTip("Generate Paddock Report …")
        self.pdfReportButton.clicked.connect(self.onGenerateReport)

        self.toolBar = QToolBar()
        self.toolBar.setMovable(False)
        self.toolBar.setFloatable(False)
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolBar.addWidget(self.currentTimeframeButton)
        self.toolBar.addWidget(self.futureTimeframeButton)
        self.toolBar.addWidget(self.sketchFenceButton)
        self.toolBar.addWidget(self.sketchPipelineButton)
        self.toolBar.addWidget(self.sketchWaterpointButton)
        self.toolBar.addWidget(self.pdfReportButton)
        self.toolBar.addWidget(self.extractCsvButton)

        self.tabWidget.setCornerWidget(self.toolBar)

        # Create a button group to control checking of the Timeframe buttons
        self.timeframeButtonGroup = QButtonGroup(exclusive=True)
        self.timeframeButtonGroup.addButton(self.currentTimeframeButton)
        self.timeframeButtonGroup.addButton(self.futureTimeframeButton)

    def refreshUi(self):
        # Update the timeframe checked thing
        if self.workspace:
            self.currentTimeframeButton.setChecked(Timeframe[self.workspace.timeframe.name] == Timeframe.Current)
            self.futureTimeframeButton.setChecked(Timeframe[self.workspace.timeframe.name] == Timeframe.Future)

    def buildUi(self):
        if self._uiBuilt:
            qgsInfo(f"{PLUGIN_NAME} already built?")

        qgsInfo(f"{PLUGIN_NAME} rebuilding PluginDockWidget …")

        self.paddocksWidget = PaddocksWidget(self.tabWidget)
        self.landTypesWidget = LandTypesWidget(self.tabWidget)
        self.fencesWidget = FencesWidget(self.tabWidget)
        self.pipelinesWidget = PipelinesWidget(self.tabWidget)
        self.waterpointsWidget = WaterpointsWidget(self.tabWidget)

        self.tabWidget.addTab(self.paddocksWidget, QIcon(f":/plugins/{PLUGIN_FOLDER}/images/paddock.png"), 'Paddocks')
        self.tabWidget.addTab(
            self.landTypesWidget,
            QIcon(f":/plugins/{PLUGIN_FOLDER}/images/land-type.png"),
            'Land Types')
        self.tabWidget.addTab(self.fencesWidget, QIcon(f":/plugins/{PLUGIN_FOLDER}/images/fence.png"), 'Fences')
        self.tabWidget.addTab(
            self.pipelinesWidget,
            QIcon(f":/plugins/{PLUGIN_FOLDER}/images/pipeline-dashed.png"),
            'Pipelines')
        self.tabWidget.addTab(
            self.waterpointsWidget,
            QIcon(f":/plugins/{PLUGIN_FOLDER}/images/waterpoint.png"),
            'Waterpoints')

        self.currentTimeframeButton.clicked.connect(lambda: self.workspace.setTimeframe("Current"))
        self.futureTimeframeButton.clicked.connect(lambda: self.workspace.setTimeframe("Future"))

        self.sketchFenceButton.clicked.connect(self.fencesWidget.sketchFence)
        self.sketchPipelineButton.clicked.connect(self.pipelinesWidget.sketchPipeline)
        self.sketchWaterpointButton.clicked.connect(self.waterpointsWidget.sketchWaterpoint)

        self.extractCsvButton.clicked.connect(self.onExtractCsv)

        self.workspace.timeframeChanged.connect(self.refreshUi)
        self.workspace.featureSelected.connect(lambda layerId: self.onFeatureSelected(layerId))
        self.workspace.lockChanged.connect(self.onLockChanged)

        self._uiBuilt = True
        qgsInfo(f"{PLUGIN_NAME} rebuilt PluginDockWidget.")

        self.refreshUi()

    def clearUi(self):
        if not self._uiBuilt:
            return

        qgsInfo(f"{PLUGIN_NAME} tearing down PluginDockWidget …")

        while (self.tabWidget.count() > 0):
            self.tabWidget.removeTab(0)

        self.paddocksWidget = None
        self.landTypesWidget = None
        self.fencesWidget = None
        self.pipelinesWidget = None
        self.waterpointsWidget = None

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

    def onGenerateReport(self):
        """Open dialog to preview and generate PDF report."""
        self.pdfReportDialog = PdfReportDialog()
        self.pdfReportDialog.setModal(True)
        self.pdfReportDialog.show()

    def onExtractCsv(self):
        """Extract the current Feature Table as CSV."""
        featureLayer = self.tabWidget.currentWidget().featureTable(0).featureLayer
        featureLayer.extractCsv()

    def onFeatureSelected(self, layerId):
        """Switch to the correct tab when a feature is selected."""

        widgets = [
            self.paddocksWidget,
            self.landTypesWidget,
            self.fencesWidget,
            self.pipelinesWidget,
            self.waterpointsWidget
        ]

        matchedWidget = next((w for w in widgets if w.hasLayerId(layerId)), None)

        if matchedWidget:
            self.tabWidget.setCurrentWidget(matchedWidget)

    def onLockChanged(self, locked):
        """Disable buttons when the workspace is locked."""
        self.currentTimeframeButton.setEnabled(not locked)
        self.futureTimeframeButton.setEnabled(not locked)
        self.sketchFenceButton.setEnabled(not locked)
        self.sketchPipelineButton.setEnabled(not locked)
        self.sketchWaterpointButton.setEnabled(not locked)

    def closeEvent(self, e):
        self.pdfReportDialog = None
