# -*- coding: utf-8 -*-

from qgis.PyQt.QtWidgets import QStyledItemDelegate

from qgis.core import QgsFeature

from ...utils import qgsDebug
from .feature_list_item import FeatureListItem

class FeatureListItemDelegate(QStyledItemDelegate):
    """A delegate that paints a FeatureListItem on a custom rectangle."""
    def __init__(self, featureLayer, parent=None):
        super().__init__(parent)
        
        self._featureLayer = featureLayer

    def createEditor(self, parent, option, index):
        super().createEditor(parent, option, index)
        
    def paint(self, painter, option, index):
        
        qgsFeature = QgsFeature()
        
        if index.model().featureByIndex(index, qgsFeature):
            feature = self._featureLayer.wrapFeature(qgsFeature)
            qgsDebug(f"FeatureListItemDelegate.paint: {feature}")

            if feature:
                featureListItem = FeatureListItem(feature)
                featureListItem.setGeometry(option.rect)

                painter.save()
                painter.translate(option.rect.x(), option.rect.y())

                featureListItem.render(painter)
                painter.restore()

    def setEditorData(self, editor, index):
        super().setEditorData(editor, index)
        
    def setModelData(self, editor, model, index):
        super().setModelData(editor, model, index)
        
    def sizeHint(self, option, index):
        return super().sizeHint(option, index)
    
    def updateEditorGeometry(self, editor, option, index):
        super().updateEditorGeometry(editor, option, index)
    
# virtual void	setEditorData(QWidget *editor, const QModelIndex &index) const override
# virtual void	setModelData(QWidget *editor, QAbstractItemModel *model, const QModelIndex &index) const override
# virtual QSize	sizeHint(const QStyleOptionViewItem &option, const QModelIndex &index) const override
# virtual void	updateEditorGeometry(QWidget *editor, const QStyleOptionViewItem &option, const QModelIndex &index) const override


