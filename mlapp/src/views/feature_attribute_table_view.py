# -*- coding: utf-8 -*-
from qgis.core import QgsVectorLayerCache
from qgis.gui import QgsAttributeTableModel, QgsAttributeTableFilterModel, QgsAttributeTableView

from ..models import WorkspaceMixin
from ..utils import qgsDebug

class FeatureAttributeTableView(QgsAttributeTableView, WorkspaceMixin):

    def __init__(self, parent=None):
        """Constructor."""
        QgsAttributeTableView.__init__(self, parent)
        WorkspaceMixin.__init__(self)

        self._featureLayer = None
        self._layerCache = None
        self._tableModel = None
        self._tableFilterModel = None

    @property
    def featureLayer(self):
        return self._featureLayer

    @featureLayer.setter
    def featureLayer(self, layer):
        self._featureLayer = layer
        self._layerCache = QgsVectorLayerCache(layer, layer.featureCount())
        self._tableModel = QgsAttributeTableModel(self._layerCache)
        self._tableModel.loadLayer()
        self._tableFilterModel = QgsAttributeTableFilterModel(
            self.workspace.iface.mapCanvas(),
            self._tableModel, parent=self._tableModel)
        self._tableFilterModel.setFilterMode(QgsAttributeTableFilterModel.ShowAll)
        self.setModel(self._tableFilterModel)
