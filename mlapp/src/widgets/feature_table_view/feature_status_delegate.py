# -*- coding: utf-8 -*-
from math import floor

from qgis.PyQt.QtCore import Qt, QRect
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QStyledItemDelegate

from ...layers.fields import FeatureStatus


class FeatureStatusDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, opt, index):
        """Paint the cell."""

        try:
            statusText = index.model().data(index, role=Qt.DisplayRole)
            featureStatus = FeatureStatus[statusText]
            self.paintFeatureStatus(painter, opt.rect, featureStatus)
        except BaseException:
            pass

        super().paint(painter, opt, index)

    def paintFeatureStatus(self, painter, cellRect, featureStatus):
        """Paint an icon in the model cell."""

        # Work in tenths-ish
        margin = round(min(cellRect.width(), cellRect.height()) * 0.1)

        # Vaguely centered here
        labelRect = QRect(cellRect.x() + margin,
                          cellRect.y() + margin,
                          cellRect.width() - 2 * margin,
                          cellRect.height() - 2 * margin)

        (r, g, b, a) = featureStatus.toColour()

        painter.fillRect(labelRect, QColor(r, g, b, a))
