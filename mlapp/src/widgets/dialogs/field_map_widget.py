

# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic

from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QPushButton, QSizePolicy, QWidget

from qgis.gui import QgsFieldComboBox

from ...layers.fields import FieldMap
from ...utils import PLUGIN_FOLDER, qgsDebug

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'field_map_widget_base.ui')))


class FieldMapWidget(QWidget, FORM_CLASS):
    f"""A widget that shows the current importable layers in the map view
        as a combobox."""

    fieldMapChanged = pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)

        self.setupUi(self)

        self.fieldMap = None
        self.mapFieldButton.clicked.connect(self.mapField)
        self.setVisible(False)

    def setLayers(self, importLayer, targetLayer):
        """Set the import layer from which to map fields."""
        
        qgsDebug(f"FieldMapWidget.setLayers({importLayer.id()}, {targetLayer.id()})")
        
        if importLayer is None or targetLayer is None:
            self.fieldMap = None

        if self.fieldMap is None or (self.fieldMap.importLayer.id() != importLayer.id()) or (self.fieldMap.targetLayer.id() != targetLayer.id()):
            self.unmapFields()
            self.fieldMap = FieldMap(importLayer, targetLayer)
            self.setVisible(True)

    def unmapFields(self):
        """Clear all mapped fields."""
        for index in range(len(self.fieldMap)):
            self.unmapField(index)
        self.fieldMap = None

    def unmapField(self, index):
        for column in range(3):
            item = self.layout().itemAtPosition(index + 1, column)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()      

    def setFields(self, importFieldName, targetFieldName):
        """Set the fields to be mapped."""
        self.fieldMap.mapFieldsByName(importFieldName, targetFieldName)
        self.fieldMapChanged.emit()

    def mapField(self, index, importFieldName=None, targetFieldName=None):
        """Map the selected import layer field to the selected target layer field."""

        if not targetFieldName and self.fieldMap.unmappedTargetFields:
            targetFieldName = next(iter(self.unmappedTargetFields)).name()

        if not targetFieldName:
            return

        importLayerFieldComboBox = QgsFieldComboBox(self)
        importLayerFieldComboBox.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        importLayerFieldComboBox.setAllowEmptyFieldName(True)
        importLayerFieldComboBox.setPlaceholderText("Select incoming field …")
        importLayerFieldComboBox.setFields(self.fieldMap.unmappedImportFields)

        targetLayerFieldComboBox = QgsFieldComboBox(self)
        targetLayerFieldComboBox.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        targetLayerFieldComboBox.setFields(self.fieldMap.unmappedTargetFields)
        targetLayerFieldComboBox.setField(targetFieldName)
        targetLayerFieldComboBox.setAllowEmptyFieldName(False)
        # targetLayerFieldComboBox.setPlaceholderText("Select imported field …")


        if targetFieldName:
            targetField = self.fieldMap.targetLayer.field(targetFieldName)
            targetLayerFieldComboBox.setField(targetFieldName)
            if targetField.required():
                # Can't change required items
                self.targetFieldComboBox.setEnabled(False)
            else:        
                removeButton = QPushButton(QIcon(f":/plugins/{PLUGIN_FOLDER}/images/trash-feature.png"), None)
                removeButton.setMinimumSize(50, 50)
                removeButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        row = index + 1

        removeButton.clicked.connect(lambda: self.unmapField(row))
        importLayerFieldComboBox.fieldChanged.connect(lambda field: self.setFields(field, targetLayerFieldComboBox.currentField()))
        targetLayerFieldComboBox.fieldChanged.connect(lambda field: self.setFields(importLayerFieldComboBox.currentField(), field))

        self.layout().addWidget(importLayerFieldComboBox, row, 0)
        self.layout().addWidget(targetLayerFieldComboBox, row, 1)
        self.layout().addWidget(removeButton, row, 2)
        
        self.adjustSize()
        self.fieldMapChanged.emit()

    def mapFields(self):
        for index in range(len(self.fieldMap)):
            self.mapField(index)
             

        
