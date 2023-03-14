# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor

from qgis.gui import QgsAttributeTableDelegate

from ...layers.fields import FeatureStatus


class FeatureStatusDelegate(QgsAttributeTableDelegate):

    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        """Paint the cell."""
        try:
            painter.save()

            statusText = index.data(role=Qt.DisplayRole)
            featureStatus = FeatureStatus(statusText)

            # cellSelected = (self._tableView.selectionModel().currentIndex().row() == index.row())

            painter.setPen(Qt.NoPen)
            # if cellSelected:
            # painter.setBrush(option.palette.highlight())
            # else:
            painter.setBrush(QColor(*featureStatus.toColour()))
            painter.fillRect(option.rect, painter.brush())
            # if cellSelected:
            #     painter.setPen(option.palette.highlightedText().color())
            # else:
            painter.setPen(QColor(*featureStatus.toForegroundColour()))
            painter.drawText(option.rect, Qt.AlignCenter, statusText)

            painter.restore()
        except BaseException:
            pass
