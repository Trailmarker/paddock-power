# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QLabel

from ...utils import getComponentStyleSheet

STYLESHEET = getComponentStyleSheet(__file__)


class ConditionTypeLabel(QLabel):

    def __init__(self, conditionType, parent=None):
        """Constructor."""
        super().__init__(parent)

        self.condtionType = conditionType

    @property
    def conditionType(self):
        return self._conditionType

    @conditionType.setter
    def conditionType(self, conditionType):
        if conditionType:
            self.conditionType = conditionType
            self.setProperty("class", conditionType.name)
            self.setStyleSheet(STYLESHEET)
            self.refreshUi()

    def refreshUi(self):
        self.setText(str(self.conditionType))
