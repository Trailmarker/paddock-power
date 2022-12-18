# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt, pyqtSignal, pyqtSlot

from ..spatial.features.feature import Feature
from ..spatial.layers.feature_layer import FeatureLayer
from ..tools.map_tool import MapTool
from ..utils import PLUGIN_NAME
from ..views.feature_view.feature_view import FeatureView
from .glitch import Glitch
from .project_base import ProjectBase

# Initialize Qt resources from file resources.py
from ...resources_rc import *


class Project(ProjectBase):
    MENU_NAME = f"&{PLUGIN_NAME}"

    # emit this signal when a selected PersistedFeature is updated
    selectedFeatureChanged = pyqtSignal(Feature)
    projectUnloading = pyqtSignal()

    def __init__(self, iface, gpkgFile=None, projectName=None):
        super().__init__(gpkgFile, projectName)

        self.iface = iface

        self.currentTool = None

        self.views = {}

    def setTool(self, tool):
        """Set the current tool for this Project."""
        if not isinstance(tool, MapTool):
            raise Glitch(
                f"The {PLUGIN_NAME} tool must be of a recognised type")

        self.unsetTool()
        self.currentTool = tool
        self.iface.mapCanvas().setMapTool(self.currentTool)

    def unsetTool(self):
        if self.currentTool is not None:
            self.currentTool.clear()
            self.currentTool.dispose()
            self.iface.mapCanvas().unsetMapTool(self.currentTool)
            self.currentTool = None

    def selectFeature(self, feature):
        self.selectedFeatureChanged.emit(feature)

    @pyqtSlot()
    def unload(self):
        """Removes the plugin menu item and icon from QGIS interface."""
        self.projectUnloading.emit()

        self.unsetTool()

        for viewType, view in self.views.values():
            self.iface.removeDockWidget(view)
            self.onCloseView(viewType)

    @pyqtSlot(FeatureLayer, list)
    def onLayerSelectionChanged(self, layer, selection):
        if len(selection) == 1:
            feature = layer.getFeature(selection[0])
            if feature is not None:
                self.selectFeature(feature)

    def openView(self, viewType, dockArea):
        if viewType not in self.views:
            view = viewType(self)
            view.closingView.connect(lambda: self.onCloseView(viewType))
            self.views[viewType] = view
            self.iface.addDockWidget(dockArea, view)
            view.show()

    @pyqtSlot()
    def openFeatureView(self):
        """Run method that loads and opens the Feature View."""
        self.openView(FeatureView, Qt.BottomDockWidgetArea)

    @pyqtSlot()
    def onCloseView(self, viewType):
        if viewType in self.views:
            del self.views[viewType]
