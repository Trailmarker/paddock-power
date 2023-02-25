# -*- coding: utf-8 -*-
from qgis.core import QgsVectorLayerCache
from qgis.gui import QgsAttributeTableFilterModel, QgsAttributeTableModel, QgsFeatureListModel, QgsFeatureListView, QgsFeatureListViewDelegate

from ..models import WorkspaceMixin


class FeatureListView(QgsFeatureListView, WorkspaceMixin):

    def __init__(self, featureLayer, editWidgetFactory, parent=None):
        """Constructor."""
        QgsFeatureListView.__init__(self, parent)
        WorkspaceMixin.__init__(self)

        self._featureLayer = featureLayer
        self._layerCache = QgsVectorLayerCache(self._featureLayer, self._featureLayer.featureCount())
        self._tableModel = QgsAttributeTableModel(self._layerCache)
        self._tableModel.loadLayer()
        self._tableFilterModel = QgsAttributeTableFilterModel(
            self.workspace.iface.mapCanvas(),
            self._tableModel, parent=self._tableModel)
        self._tableFilterModel.setFilterMode(QgsAttributeTableFilterModel.ShowAll)
        self._listModel = QgsFeatureListModel(self._tableFilterModel)
        self._listModel.setDisplayExpression('"Name"')
        self._featureListViewDelegate = QgsFeatureListViewDelegate(self._listModel)
        self.setItemDelegate(self._featureListViewDelegate)
        self.setModel(self._listModel)
