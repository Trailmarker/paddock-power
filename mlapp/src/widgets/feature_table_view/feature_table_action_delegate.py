# -*- coding: utf-8 -*-
from math import floor

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QBrush, QPainter
from qgis.PyQt.QtWidgets import QStyledItemDelegate


class FeatureTableActionDelegate(QStyledItemDelegate):

    def __init__(self, tableView, featureTableActionModel, parent=None):
        super().__init__(parent)
        self._tableView = tableView
        self._actionModel = featureTableActionModel

    @property
    def featureTableActionModel(self):
        """The model for the action."""
        return self._actionModel

    def paint(self, painter, option, index):
        """Paint the cell."""
        try:
            brush = painter.brush()
            cellSelected = (self._tableView.selectionModel().currentIndex().row() == index.row())

            cellColor = option.palette.highlight().color() if cellSelected else Qt.transparent
            painter.fillRect(option.rect, QBrush(cellColor))

            icon = self.featureTableActionModel.icon(index)
            self.paintIcon(painter, option.rect, icon)

            # Restore brush
            painter.setBrush(brush)
        except BaseException:
            pass

    def paintIcon(self, painter, cellRect, icon):
        """Paint an icon in the model cell."""
        # TODO should really be able to change the colour in which the icon is painted
        # painter.setCompositionMode(QPainter.CompositionMode_SourceIn)

        # Work in fifths-ish
        dim = round(min(cellRect.width(), cellRect.height()) * 0.4)

        pixmap = icon.pixmap(dim, dim)
        painter.drawPixmap(floor(cellRect.x() + (cellRect.width() - dim) / 2),
                           floor(cellRect.y() + (cellRect.height() - dim) / 2),
                           pixmap)
