# -*- coding: utf-8 -*-
from math import floor
from qgis.PyQt.QtWidgets import QStyledItemDelegate

from .feature_table_action import FeatureTableActionModelFactory


class FeatureTableActionDelegate(QStyledItemDelegate):

    def __init__(self, featureTableAction, editWidgetFactory=None, parent=None):
        super().__init__(parent)
        self._actionModel = FeatureTableActionModelFactory(editWidgetFactory).createModel(featureTableAction, parent)

    @property
    def actionModel(self):
        """The model for the action."""
        return self._actionModel

    def paint(self, painter, option, index):
        """Paint the cell."""
        super().paint(painter, option, index)

        # icon = self.actionModel.icon(index)
        # if icon:
        #     self.paintIcon(painter, option.rect, icon)

    def paintIcon(self, painter, cellRect, icon):
        """Paint an icon in the model cell."""

        # Work in fifths-ish
        dim = min(cellRect.width(), cellRect.height()) * 0.4

        pixmap = icon.pixmap(dim, dim)
        painter.drawPixmap(floor(cellRect.x() + (cellRect.width() - dim) / 2),
                           floor(cellRect.y() + (cellRect.height() - dim) / 2),
                           pixmap)
