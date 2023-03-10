# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QStyledItemDelegate

from ...utils import qgsDebug


class FeatureIconDelegate(QStyledItemDelegate):

    def __init__(self, icon, parent=None):
        QStyledItemDelegate.__init__(self, parent)

        self._icon = icon

    def paint(self, painter, option, index):
        qgsDebug(f"Painting {index.row()}, {index.column()}")

        cellRect = option.rect

        # Work in fifths-ish
        dim = min(cellRect.width(), cellRect.height()) * 0.4

        pixmap = self._icon.pixmap(dim, dim)
        painter.drawPixmap(cellRect.x() + (cellRect.width() - dim) / 2,
                           cellRect.y() + (cellRect.height() - dim) / 2, pixmap)
