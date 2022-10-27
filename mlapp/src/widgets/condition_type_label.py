# -*- coding: utf-8 -*-

from qgis.PyQt.QtWidgets import QLabel

from ..models.colors import toCssColour
from ..models.glitch import Glitch
from ..spatial.schemas.condition_type import ConditionType


class ConditionTypeLabel(QLabel):

    def __init__(self, conditionType, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.setConditionType(conditionType)

    def setConditionType(self, conditionType):
        if conditionType is not None and not isinstance(conditionType, ConditionType):
            raise Glitch(
                "Your Condition record's condition type must be a valid ConditionType value.")

        self.conditionType = conditionType
        self.refreshUi()

    def refreshStylesheet(self):
        background = toCssColour(*self.conditionType.toColour())
        foreground = toCssColour(*self.conditionType.toForegroundColour())

        stylesheet = (f"QLabel {{\n"
                      f"     background-color: {background};\n"
                      f"     color: {foreground};\n"
                      f"     border-radius: 2px;\n"
                      f"     margin: 2px;\n"
                      f"     padding: 2px;\n"
                      f"}}\n")

        self.setStyleSheet(stylesheet)

    def refreshUi(self):
        if self.conditionType is None:
            self.setVisible(False)
            return

        self.setVisible(True)
        self.refreshStylesheet()
        self.setText(str(self.conditionType))
