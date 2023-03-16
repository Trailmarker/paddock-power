# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QPushButton

from qgis.gui import QgsFieldComboBox

from ...layers.fields import FieldMap
from ...models import WorkspaceMixin
from .dialog import Dialog

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'import_dialog_base.ui')))


class ImportDialog(QDialog, FORM_CLASS, WorkspaceMixin):
    def __init__(self, parent=None):
        """Constructor."""
        Dialog.__init__(self, parent)
        FORM_CLASS.__init__(self)
        WorkspaceMixin.__init__(self)

        self.setupUi(self)

        self._fieldMap = None
        self._targetLayer = None
        self._importLayer = None

        self._importLayerFieldComboBoxes = []
        self._targetLayerFieldComboBoxes = []
        self._unmapFieldButtons = []

        self.importLayerComboBox.currentIndexChanged.connect(self.setImportLayer)
        self.targetLayerComboBox.currentIndexChanged.connect(self.setTargetLayer)
        self.mapFieldButton.clicked.connect(self.mapField)

    def mapField(self):
        row = self.fieldMapGrid.addRow()  # TODO
        importLayerFieldComboBox = QgsFieldComboBox(self._importLayer)
        targetLayerFieldComboBox = QgsFieldComboBox(self._targetLayer)
        unmapFieldButton = QPushButton("Remove")

    def populateImportLayerComboBox(self):
        #self.importLayerComboBox.addItem("Select …", None)
        pass

    def populateImportAsComboBox(self):
        self.targetLayerComboBox.addItem("Select …", None)

        importableFeatureLayers = self.workspace.workspaceLayers.importableFeatureLayers()
        for layer in importableFeatureLayers:
            self.targetLayerComboBox.addItem(layer.defaultName(), layer)

        self.targetLayerComboBox.setCurrentIndex(0)

    def populateFieldMap(self):
        if not self._targetLayer or not self._importLayer:
            self._fieldMap = None
            return

        self._fieldMap = FieldMap(self._importLayer, self._targetLayer)

    def populateFieldMapGrid(self):
        if not self._fieldMap:
            self.fieldMapGrid.setVisible(False)
            self.fieldMapGrid.clear()
            return

        # TODO figure out how to add combo boxes from both sides

    def setImportLayer(self, layer):
        self._importLayer = layer

    def setTargetLayer(self, layer):
        self._targetLayer = layer

    def validateAndImport(self):
        """Validate the field mappings and do the import."""

    # def closeEvent(self, event):
    #     self.
    #     event.accept()

    @property
    def dialogRole(self):
        return "Import"

    def reject(self):
        super().reject()
