# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QStyledItemDelegate


from ...layers.fields import FeatureStatus


class FeatureStatusDelegate(QStyledItemDelegate):

    def __init__(self, tableView, parent=None):
        super().__init__(parent)
        
        # Cheeky! But couldn't get the selection otherwise
        # option.state & QStyle.State_Selected does not work
        self._tableView = tableView

    def paint(self, painter, option, index):
        """Paint the cell."""
        try:
            painter.save()

            statusText = index.data(role=Qt.DisplayRole)
            featureStatus = FeatureStatus[statusText]

            cellSelected = (self._tableView.selectionModel().currentIndex().row() == index.row())

            if cellSelected:
                painter.setPen(Qt.white)
                painter.setBrush(option.palette.highlight())
            else:
                painter.setPen(QColor(*featureStatus.toForegroundColour()))
                painter.setBrush(QColor(*featureStatus.toColour()))

            painter.fillRect(option.rect, painter.brush())
            painter.drawText(option.rect, Qt.AlignCenter, statusText)

            painter.restore()
        except BaseException:
            pass