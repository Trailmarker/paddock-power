

# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic

from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QPushButton, QSizePolicy, QWidget

from qgis.core import QgsFields
from qgis.gui import QgsFieldComboBox

from ...layers.fields import FieldMap
from ...utils import PLUGIN_FOLDER, getComponentStyleSheet, qgsDebug

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'field_map_widget_base.ui')))


STYLESHEET = getComponentStyleSheet(__file__)


class FieldMapWidget(QWidget, FORM_CLASS):
    f"""A widget that shows the current importable layers in the map view
        as a combobox."""

    fieldMapChanged = pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        FORM_CLASS.__init__(self)

        self.setupUi(self)

        self.setStyleSheet(STYLESHEET)

        self.fieldMap = None
        self.addFieldButton.clicked.connect(self.addFieldUi)

    @property
    def hasFieldMap(self):
        return self.fieldMap is not None

    def resetFieldMap(self, importLayer, targetLayer):
        """Set the import layer from which to map fields."""
        if importLayer and targetLayer and self.fieldMap and self.fieldMap.importLayer.id(
        ) == importLayer.id() and self.fieldMap.targetLayer.id() == targetLayer.id():
            return

        self.removeFieldMapUi()
        if importLayer and targetLayer:
            self.fieldMap = FieldMap(importLayer, targetLayer)
            self.setupFieldMapUi()
        else:
            self.fieldMap = None

    def updateFieldMap(self, index, importFieldName, targetFieldName):
        """Set the fields to be mapped."""
        self.removeFieldMapUi()
        self.fieldMap.update(index, importFieldName, targetFieldName)
        self.setupFieldMapUi()

    def removeFieldUi(self, index):
        for column in range(3):
            item = self.layout().itemAtPosition(index + 1, column)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()

    def removeFieldMapUi(self):
        if self.hasFieldMap:
            for index in range(len(self.fieldMap)):
                self.removeFieldUi(index)

    def addFieldUi(self):
        """Add a new field mapping row to the user interface."""
        qgsDebug(f"addFieldUi")
        if self.hasFieldMap:
            qgsDebug(f"addFieldUi: got field map")
            self.setupFieldUi(len(self.fieldMap))

    def setupFieldUi(self, index, importField=None, targetField=None):
        """Map the selected import layer field to the selected target layer field."""

        if not targetField:
            targetField = self.fieldMap.nextUnmappedTargetField

        if not targetField:
            return

        importLayerFieldComboBox = QgsFieldComboBox(self)
        importLayerFieldComboBox.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        importLayerFieldComboBox.setAllowEmptyFieldName(True)
        importLayerFieldComboBox.setPlaceholderText("Select incoming field …")
        importLayerFieldComboBox.setFields(self.fieldMap.importQgsFields)

        if importField is not None:
            importLayerFieldComboBox.setField(importField.name())

        targetLayerFieldComboBox = QgsFieldComboBox(self)
        targetLayerFieldComboBox.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        targetLayerFieldComboBox.setAllowEmptyFieldName(False)
        targetLayerFieldComboBox.setPlaceholderText("Select target field …")
        targetLayerFieldComboBox.setFields(self.fieldMap.targetQgsFields)
        targetLayerFieldComboBox.setField(targetField.name())

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
            removeButton.clicked.connect(lambda: self.removeFieldUi(index))

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

    def setupFieldMapUi(self):
        """Build the mapping user interface from the current field map."""
        if self.hasFieldMap:
            for (index, (importField, targetField)) in enumerate(self.fieldMap):
                self.setupFieldUi(index, importField, targetField)
