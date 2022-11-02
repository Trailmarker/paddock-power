# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QTabBar, QPushButton

from ..view_base import ViewBase
from ..fence_view.fence_widget import FenceWidget
from ..paddock_view.paddock_widget import PaddockWidget
from ..pipeline_view.pipeline_widget import PipelineWidget
from ..waterpoint_view.waterpoint_widget import WaterpointWidget

from .feature_tab_widget import FeatureTabWidget

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'feature_view_base.ui')))


class FeatureView(ViewBase, FORM_CLASS):

    def __init__(self, project, parent=None):
        """Constructor."""
        super().__init__(project, parent)

        self.setupUi(self)

        self.fenceTab = FenceWidget(project, self)
        self.paddockTab = PaddockWidget(project, self)
        self.pipelineTab = PipelineWidget(project, self)
        self.waterpointTab = WaterpointWidget(project, self)

        # self.tabWidget.addTab(self.fenceTab, QIcon(":/plugins/mlapp/images/split-paddock.png"), 'Fences')
        self.tabWidget.addTab(self.paddockTab, QIcon(":/plugins/mlapp/images/split-paddock.png"), 'Paddocks')
        self.tabWidget.addTab(self.pipelineTab, QIcon(":/plugins/mlapp/images/split-paddock.png"), 'Pipelines')
        self.tabWidget.addTab(self.waterpointTab, QIcon(":/plugins/mlapp/images/split-paddock.png"), 'Waterpoints')

        # Experimentation with customising the tab bar
        # self.tabWidget.setCornerWidget(QPushButton('Add Feature'), Qt.TopLeftCorner)

        # tabBar = self.tabWidget.findChild(QTabBar)
        # tabBar.hide()


