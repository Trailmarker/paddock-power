# # -*- coding: utf-8 -*-
# from math import floor

# from qgis.PyQt.QtCore import Qt 
# from qgis.PyQt.QtGui import QColor, QIcon, QPainter
# from qgis.PyQt.QtWidgets import QStyledItemDelegate


# class FeatureTableActionDelegate(QStyledItemDelegate):

#     def __init__(self, tableView, featureTableActionModel, parent=None):
#         super().__init__(parent)
#         self._tableView = tableView
#         self._actionModel = featureTableActionModel

#     @property
#     def featureTableActionModel(self):
#         """The model for the action."""
#         return self._actionModel

#     def paint(self, painter, option, index):
#         """Paint the cell."""
#         try:
#             icon = self.featureTableActionModel.icon(index)
#             if icon:
#                 painter.save()
            
#                 # If cell is selected, we 'negative' the icon (or try to)
#                 cellSelected = (self._tableView.selectionModel().currentIndex().row() == index.row())            
#                 if cellSelected:                
#                     painter.setBrush(option.palette.highlight())
#                     painter.fillRect(option.rect, painter.brush())
#                     # self.paintInvertedIcon(painter, option.rect, icon)
#                 # else:
#                 self.paintIcon(painter, option.rect, icon)
            
#                 painter.restore()
#         except BaseException:
#             pass
        
#     def paintIcon(self, painter, cellRect, icon):
#         """Paint an icon in the model cell."""
#         # Work in fifths-ish
#         dim = round(min(cellRect.width(), cellRect.height()) * 0.6)

#         pixmap = icon.pixmap(dim, dim)
#         painter.drawPixmap(floor(cellRect.x() + (cellRect.width() - dim) / 2),
#                            floor(cellRect.y() + (cellRect.height() - dim) / 2),
#                            pixmap)

#     def paintInvertedIcon(self, painter, cellRect, icon):
#         """Paint an icon in the model cell."""
#         # Work in fifths-ish
#         dim = round(min(cellRect.width(), cellRect.height()) * 0.6)

#         pixmap = icon.pixmap(dim, dim)

#         painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
#         painter.setBrush(Qt.white)
#         painter.setPen(Qt.NoPen)

#         painter.drawPixmap(floor(cellRect.x() + (cellRect.width() - dim) / 2),
#                            floor(cellRect.y() + (cellRect.height() - dim) / 2),
#                            pixmap)
