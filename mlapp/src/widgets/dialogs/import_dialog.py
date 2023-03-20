# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QPushButton

from qgis.core import QgsProject
from qgis.gui import QgsFieldComboBox

from ...layers.fields import FieldMap
from ...layers.interfaces import IMapLayer, IImportableFeatureLayer
from ...models import WorkspaceMixin
from .dialog import Dialog

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'import_dialog_base.ui')))


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

        # Importable layers are only the instances of IImportableFeatureLayer so again
        # get the opposite
        nonImportableLayers = [layer for layer in QgsProject.instance().mapLayers().values()
                               if not isinstance(layer, IImportableFeatureLayer)]

        self.targetLayerComboBox.setExceptedLayerList(nonImportableLayers)
        self.targetLayerComboBox.setAllowEmptyLayer(True)

        for i in range(self.targetLayerComboBox.count()):
            targetLayer = self.targetLayerComboBox.itemData(i)
            if targetLayer:
                self.targetLayerComboBox.setItemIcon(i, targetLayer.icon())

        self.fieldMapWidget.layout().setContentsMargins(0, 0, 0, 0)

        self.cancelButton.clicked.connect(self.reject)
        self.importButton.clicked.connect(self.importFeatures)
        self.importLayerComboBox.layerChanged.connect(self.setLayers)
        self.targetLayerComboBox.layerChanged.connect(self.setLayers)
        self.fieldMapWidget.fieldMapChanged.connect(self.adjustSize)

    def adjustSize(self):
        self.fieldMapWidget.adjustSize()
        super().adjustSize()

    def setLayers(self):
        """Set the import layer from which to map fields."""
        (importLayer, targetLayer) = (self.importLayerComboBox.currentLayer(), self.targetLayerComboBox.currentLayer())
        self.fieldMapWidget.setLayers(importLayer, targetLayer)
        if importLayer:
            self.setWindowTitle(importLayer.name())

    def importFeatures(self):
        """Validate the field mappings and do the import."""
        self.workspace.importFeatures(
            self.targetLayerComboBox.currentLayer(),
            self.importLayerComboBox.currentLayer(),
            self.fieldMapWidget.fieldMap)

    @property
    def dialogRole(self):
        return "Import"
