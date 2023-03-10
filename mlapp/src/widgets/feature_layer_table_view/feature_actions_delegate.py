# # -*- coding: utf-8 -*-
# from qgis.PyQt.QtWidgets import QStyledItemDelegate

# from ...utils import qgsDebug

# class FeatureActionsDelegate(QStyledItemDelegate):
    
#     def __init__(self, feature, parent=None):
#         QStyledItemDelegate.__init__(self, parent)

#         self._icon = icon
#         # self._callback = callback


#     def paint(self, painter, option, index):
#         qgsDebug(f"Painting {index.row()}, {index.column()}")
        
#         cellRect = option.rect
        
#         # Work in fifths-ish
#         dim = min(cellRect.width(), cellRect.height()) * 0.4
        
#         pixmap = self._icon.pixmap(dim, dim)
#         painter.drawPixmap(cellRect.x() + (cellRect.width() - dim)/2, cellRect.y() + (cellRect.height() - dim)/2, pixmap)
               
# #         QPainter painter(this);
# #         QPixmap pxm = m_icon.pixmap(height() - 6, height() - 6);
# #         int x = 2, cx = pxm.width();

# #         painter.drawPixmap(x, 3, pxm);
# #         painter.setPen(QColor("lightgrey"));
# #         painter.drawLine(cx + 2, 3, cx + 2, height() - 4);
        
