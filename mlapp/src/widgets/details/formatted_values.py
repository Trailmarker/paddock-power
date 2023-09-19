# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QLabel


class FormattedValues(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)

    def setValues(self, formatSpec: str, *values):
        if values and all(value is not None for value in values) and formatSpec is not None:
            formattedValues = formatSpec.format(*values)
            super().setText(formattedValues)
        else:
            super().setText("")
        return self
