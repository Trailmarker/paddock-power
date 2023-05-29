# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QLabel


class FormattedValues(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)

    def setValues(self, formatSpec: str, *values):
        if values and all(values) and formatSpec is not None:
            super().setText(formatSpec.format(*values))
        else:
            super().setText("")
        return self
