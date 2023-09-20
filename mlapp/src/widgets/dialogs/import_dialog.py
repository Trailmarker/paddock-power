# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic

from qgis.core import QgsMapLayerProxyModel, QgsProject, QgsRasterLayer, QgsVectorLayer

from ...layers.interfaces import IMapLayer, IImportableFeatureLayer, IImportableLayer
from ...utils import getComponentStyleSheet
from .dialog import Dialog

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'import_dialog_base.ui')))


STYLESHEET = getComponentStyleSheet(__file__)


class ImportDialog(Dialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        Dialog.__init__(self, parent)
        FORM_CLASS.__init__(self)

        self.setupUi(self)

        # Import layers could be anythning that's not a workspace layer, so the 'blacklist'
        # is the workspace
        workspaceLayers = [layer for layer in QgsProject.instance().mapLayers().values()
                           if isinstance(layer, IMapLayer)]

        self.importLayerComboBox.setExceptedLayerList(workspaceLayers)
        self.importLayerComboBox.setAllowEmptyLayer(True)

        self.importPaddocksFirstLabel.setVisible(not self.workspace.hasBasePaddocks)

        exceptedTargetLayers = []
        if self.workspace.hasBasePaddocks:
            exceptedTargetLayers = [layer for layer in QgsProject.instance().mapLayers().values()
                                    if not isinstance(layer, IImportableLayer)]

        else:
            exceptedTargetLayers = [
                layer for layer in QgsProject.instance().mapLayers().values() if layer.id() not in [
                    self.workspace.basePaddockLayer.id(),
                    self.workspace.elevationLayer.id()]]

        self.targetLayerComboBox.setExceptedLayerList(exceptedTargetLayers)
        self.targetLayerComboBox.setAllowEmptyLayer(True)

        for i in range(self.targetLayerComboBox.count()):
            targetLayer = self.targetLayerComboBox.itemData(i)
            if targetLayer:
                self.targetLayerComboBox.setItemIcon(i, targetLayer.icon())

        self.fieldMapWidget.layout().setContentsMargins(0, 0, 0, 0)

        # Base appearance
        self.setStyleSheet(STYLESHEET)

        self.cancelButton.clicked.connect(self.reject)
        self.importButton.clicked.connect(self.importLayer)
        self.importLayerComboBox.layerChanged.connect(self.setImportLayer)
        self.targetLayerComboBox.layerChanged.connect(self.setTargetLayer)
        self.fieldMapWidget.fieldMapChanged.connect(self.adjustSize)

        # Initialise the field map widget
        self.setImportLayer()
        self.setTargetLayer()

        # Ensure the target layer combo box and labels are set up correctly
        self.update()

    def adjustSize(self):
        self.fieldMapWidget.adjustSize()
        super().adjustSize()

    def setImportLayer(self):
        """Set the import layer from which to map fields."""
        (importLayer, targetLayer) = (self.importLayerComboBox.currentLayer(), self.targetLayerComboBox.currentLayer())

        if isinstance(importLayer, QgsVectorLayer) and isinstance(targetLayer, IImportableFeatureLayer):
            self.fieldMapWidget.setVisible(True)
            self.fieldMapWidget.resetFieldMap(importLayer, targetLayer)
        else:
            self.fieldMapWidget.setVisible(False)

    def setTargetLayer(self):
        """Set the target layer from which to map fields."""
        targetLayer = self.targetLayerComboBox.currentLayer()

        if targetLayer:
            self.setWindowTitle(targetLayer.name())
            self.importButton.setText(f"Import {targetLayer.name()}")

        if isinstance(targetLayer, IImportableFeatureLayer):
            self.importLayerComboBox.setFilters(QgsMapLayerProxyModel.VectorLayer)
            importLayer = self.importLayerComboBox.currentLayer()
            if isinstance(importLayer, QgsVectorLayer):
                self.fieldMapWidget.setVisible(True)
                self.fieldMapWidget.resetFieldMap(importLayer, targetLayer)
        else:
            self.importLayerComboBox.setFilters(QgsMapLayerProxyModel.RasterLayer)
            self.fieldMapWidget.setVisible(False)

    def importLayer(self):
        """Validate inputs and either import elevation or features."""
        importLayer = self.importLayerComboBox.currentLayer()
        targetLayer = self.targetLayerComboBox.currentLayer()

        if isinstance(importLayer, QgsVectorLayer) and isinstance(targetLayer, IImportableFeatureLayer):
            self.workspace.importFeatureLayer(
                self.targetLayerComboBox.currentLayer(),
                self.importLayerComboBox.currentLayer(),
                self.fieldMapWidget.fieldMap)
        elif isinstance(importLayer, QgsRasterLayer):
            self.workspace.importElevationLayer(self.importLayerComboBox.currentLayer())

        super().accept()

    @property
    def dialogRole(self):
        return "Import"
