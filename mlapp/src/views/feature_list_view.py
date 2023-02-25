# -*- coding: utf-8 -*-
from qgis.core import QgsVectorLayerCache
from qgis.gui import QgsAttributeTableFilterModel, QgsAttributeTableModel, QgsFeatureListModel, QgsFeatureListView, QgsFeatureListViewDelegate

from ..models import WorkspaceMixin
from ..utils import qgsDebug
from ..widgets.feature_list.feature_list_item_delegate import FeatureListItemDelegate

class FeatureListView(QgsFeatureListView, WorkspaceMixin):

    def __init__(self, featureLayer, parent=None):
        """Constructor."""
        QgsFeatureListView.__init__(self, parent)
        WorkspaceMixin.__init__(self)

        self._featureLayer = featureLayer
        
        qgsDebug(f"FeatureListView.__init__: {self._featureLayer.featureCount()}")
         
        self._layerCache = QgsVectorLayerCache(self._featureLayer, self._featureLayer.featureCount())
        self._tableModel = QgsAttributeTableModel(self._layerCache)
        self._tableModel.loadLayer()
        self._tableFilterModel = QgsAttributeTableFilterModel(
            self.workspace.iface.mapCanvas(),
            self._tableModel, parent=self._tableModel)
        self._tableFilterModel.setFilterMode(QgsAttributeTableFilterModel.ShowAll)
        self._listModel = QgsFeatureListModel(self._tableFilterModel)
    
        self.setModel(self._listModel)

        self._featureListViewDelegate = FeatureListItemDelegate(self._featureLayer)
        self.setItemDelegate(self._featureListViewDelegate)
        
        self._layerCache.setFullCache(True)
        
        
        # self.dataChanged(self._listModel.index(0), self._listModel.index(self._listModel.rowCount()), [])
        
        # self.setIndexWidget(self._listModel.index(0, self._listModel.rowCount()), OtherFeatureListItem())
        
    def dataChanged(self, top, bottom, _):
        qgsDebug(f"FeatureListView.dataChanged: {top.row()} - {bottom.row()}")
        
        # for row in range(top.row(), bottom.row()):
        #     feature = self._listModel.data(row)
        #     self.setIndexWidget(self._listModel.index(row), OtherFeatureListItem(feature))
 
        # print("dataChanged")
        # QPushButton *pPushButton = qobject_cast<QPushButton*>(indexWidget(topLeft));
        # if (pPushButton)
        #     pPushButton->setText(model()->data(topLeft, Qt::DisplayRole).toString());
        # else
        #     QTableView::dataChanged(topLeft, bottomRight, roles);
        # QgsFeatureListView.dataChanged(self, top, bottom, roles)
