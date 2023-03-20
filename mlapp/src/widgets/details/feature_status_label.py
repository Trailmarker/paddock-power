# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QLabel

from ...utils import getComponentStyleSheet

STYLESHEET = getComponentStyleSheet(__file__)


class FeatureStatusLabel(QLabel):

    def __init__(self, status, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.status = status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if status is not None:
            self._status = status
            self.setProperty("class", status.name)
            self.setStyleSheet(STYLESHEET)
            self.refreshUi()

    def refreshUi(self):
        self.setText(str(self.status))
