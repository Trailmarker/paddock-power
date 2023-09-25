# -*- coding: utf-8 -*-
from enum import Enum

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor

from qgis.gui import QgsAttributeTableDelegate

from ...models import Glitch


class FieldDomainDelegate(QgsAttributeTableDelegate):
    """A delegate that paints the cell with the colours of a colour-coded DomainType."""

    def __init__(self, fieldDomainType, parent=None):
        super().__init__(parent)

        if not issubclass(fieldDomainType, Enum):
            raise Glitch(
                f"In FieldDomainDelegate, fieldDomainType must be a subclass of FieldDomain, not {fieldDomainType.__name__}")

        self.fieldDomainType = fieldDomainType

    def paint(self, painter, option, index):
        """Paint the cell."""
        try:
            painter.save()

            fieldDomainValueText = index.data(role=Qt.DisplayRole)
            fieldDomainValue = self.fieldDomainType(fieldDomainValueText)

            # cellSelected = (self._tableView.selectionModel().currentIndex().row() == index.row())

            painter.setPen(Qt.NoPen)
            # if cellSelected:
            # painter.setBrush(option.palette.highlight())
            # else:
            painter.setBrush(QColor(*fieldDomainValue.toColour()))
            painter.fillRect(option.rect, painter.brush())
            # if cellSelected:
            #     painter.setPen(option.palette.highlightedText().color())
            # else:
            painter.setPen(QColor(*fieldDomainValue.toForegroundColour()))
            painter.drawText(option.rect, Qt.AlignCenter, fieldDomainValue.value)

            painter.restore()
        except BaseException:
            pass
