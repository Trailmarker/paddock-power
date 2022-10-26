# -*- coding: utf-8 -*-

from qgis.PyQt.QtWidgets import QLabel

from ..models.colors import toCssColour
from ..models.glitch import Glitch
from ..spatial.schemas.feature_status import FeatureStatus


class FeatureStatusLabel(QLabel):

    def __init__(self, status, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setStatus(status)

    def setStatus(self, status):
        if status is not None and not isinstance(status, FeatureStatus):
            raise Glitch(
                "FeatureStatusLabel.__init__: status must be a FeatureStatus")

        self.status = status
        self.refreshUi()

    def refreshStylesheet(self):
        background = toCssColour(*self.status.toColour())
        foreground = toCssColour(*self.status.toForegroundColour())

        stylesheet = (f"QLabel {{\n"
                      f"     background-color: {background};\n"
                      f"     color: {foreground};\n"
                      f"     border-radius: 2px;\n"
                      f"     margin: 2px;\n"
                      f"     padding: 2px;\n"
                      f"}}\n")

        self.setStyleSheet(stylesheet)

    def refreshUi(self):
        if self.status is None:
            self.setVisible(False)
            return

        self.setVisible(True)
        self.refreshStylesheet()
        self.setText(str(self.status))
