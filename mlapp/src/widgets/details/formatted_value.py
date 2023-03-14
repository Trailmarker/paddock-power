# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QLabel


class FormattedValue(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)

    def setValue(self, value, formatSpec=None):
        if value is not None:
            if formatSpec is not None:
                super().setText(formatSpec.format(value))
            else:
                super().setText(str(value))
        else:
            super().setText("")
