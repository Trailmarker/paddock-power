

# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic

from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QPushButton, QSizePolicy, QWidget

from qgis.core import QgsFields
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
        self.mapFieldButton.clicked.connect(lambda: self.mapField(len(self.fieldMap)))

    def setLayers(self, importLayer, targetLayer):
        """Set the import layer from which to map fields."""
        if importLayer and targetLayer and (
            self.fieldMap is None or (
                self.fieldMap.importLayer.id() != importLayer.id() or self.fieldMap.targetLayer.id() != targetLayer.id()
            )
        ):
            self.resetFieldMap(importLayer, targetLayer)

    def resetFieldMap(self, importLayer, targetLayer):
        """Clear all mapped fields."""
        if importLayer is None or targetLayer is None:
            self.fieldMap = None
            return
        qgsDebug(f"FieldMapWidget.resetFieldMap({importLayer.id()}, {targetLayer.id()})")
        self.fieldMap = FieldMap(importLayer, targetLayer)
        self.update()

    def unmapField(self, index):
        for column in range(3):
            item = self.layout().itemAtPosition(index + 1, column)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()

    def updateFieldMap(self, index, importFieldName, targetFieldName):
        """Set the fields to be mapped."""
        self.fieldMap.update(index, importFieldName, targetFieldName)
        self.update()

    def buildFieldMap(self):
        """Build the mapping user interface from the current field map."""
        for (index, (importField, targetField)) in enumerate(self.fieldMap):
            self.mapField(index, importField, targetField)
        self.adjustSize()

    def mapField(self, index, importField=None, targetField=None):
        """Map the selected import layer field to the selected target layer field."""

        if not targetField:
            targetField = next(iter(self.fieldMap.unmappedTargetFields), None)

        if not targetField:
            return

        importLayerFieldComboBox = QgsFieldComboBox(self)
        importLayerFieldComboBox.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        importLayerFieldComboBox.setAllowEmptyFieldName(True)
        importLayerFieldComboBox.setPlaceholderText("Select incoming field …")
        importLayerFieldComboBox.setFields(self.fieldMap.unmappedImportFields)

        if importField:
            importLayerFieldComboBox.setField(importField.name())

        targetLayerFieldComboBox = QgsFieldComboBox(self)
        targetLayerFieldComboBox.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        targetLayerFieldComboBox.setFields(self.fieldMap.unmappedTargetFields)
        targetLayerFieldComboBox.setField(targetField.name())
        targetLayerFieldComboBox.setAllowEmptyFieldName(False)

        removeButton = None
        
        if targetField.required():
            # Can't change required items
            singleField = QgsFields()
            singleField.append(targetField)
            targetLayerFieldComboBox.setFields(singleField)
            # targetLayerFieldComboBox.setEnabled(False)
        else:
            removeButton = QPushButton(QIcon(f":/plugins/{PLUGIN_FOLDER}/images/trash-feature.png"), None)
            removeButton.setMinimumSize(50, 50)
            removeButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            removeButton.clicked.connect(lambda: self.unmapField(row))

        row = index + 1

        importLayerFieldComboBox.fieldChanged.connect(
            lambda field: self.updateFieldMap(index,
                field, targetLayerFieldComboBox.currentField()))
        targetLayerFieldComboBox.fieldChanged.connect(
            lambda field: self.updateFieldMap(index,
                importLayerFieldComboBox.currentField(), field))

        self.layout().addWidget(importLayerFieldComboBox, row, 0)
        self.layout().addWidget(targetLayerFieldComboBox, row, 1)
        if removeButton:
            self.layout().addWidget(removeButton, row, 2)

    def update(self):
        if self.fieldMap:
            for index in range(len(self.fieldMap)):
                self.unmapField(index)

            self.buildFieldMap()

        super().update()
