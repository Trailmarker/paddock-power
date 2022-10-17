# -*- coding: utf-8 -*-

from qgis.PyQt.QtWidgets import QLabel

from ..models.paddock_power_error import PaddockPowerError
from ..spatial.features.feature_status import FeatureStatus, toCssColour
from ..utils import qgsDebug

class FeatureStatusLabel(QLabel):

    def __init__(self, status, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setStatus(status)

    def setStatus(self, status):
        if status is not None and not isinstance(status, FeatureStatus):
            raise PaddockPowerError(
                "FeatureStatusLabel.__init__: status must be a FeatureStatus")

        self.status = status
        self.refreshUi()

    def refreshUi(self):
        if self.status is None:
            self.setVisible(False)
            return

        self.setVisible(True)

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
        self.setText(self.status.name)
