# -*- coding: utf-8 -*-

from qgis.core import QgsVectorLayerCache
from qgis.gui import QgsAttributeTableModel, QgsAttributeTableView, QgsAttributeTableFilterModel
from qgis.utils import iface

from ...models import QtAbstractMeta, WorkspaceMixin
from ...layers.fields import Timeframe

# See https://webgeodatavore.github.io/pyqgis-samples/gui-group/QgsAttributeTableFilterModel.html
# layer = iface.activeLayer()
# canvas = iface.mapCanvas()
# vector_layer_cache = QgsVectorLayerCache(layer, 10000)
# attribute_table_model = QgsAttributeTableModel(vector_layer_cache)
# attribute_table_model.loadLayer()

# attribute_table_filter_model = QgsAttributeTableFilterModel(
#     canvas,
#     attribute_table_model
# )
# attribute_table_view = QgsAttributeTableView()
# attribute_table_view.setModel(attribute_table_filter_model)

# attribute_table_view.show()

# # Or display the attribute_table_model with QTableView (pure QT solution)
# table_view = QTableView()
# table_view.setModel(attribute_table_model)
# table_view.show()


class FeatureTableView(QgsAttributeTableView, WorkspaceMixin, metaclass=QtAbstractMeta):
    
    def __init__(self, parent=None):
        QgsAttributeTableView.__init__(self, parent)
        WorkspaceMixin.__init__(self)
        
        self._featureLayer = None
        self._featureCache = None
        self._tableModel = None
        self._tableFilterModel = None
    
    @property
    def featureLayer(self):
        return self._featureLayer
    
    @featureLayer.setter
    def featureLayer(self, layer):
        self._featureLayer = layer
        self._featureCache = QgsVectorLayerCache(layer, layer.featureCount())
        self._tableModel = QgsAttributeTableModel(self._featureCache)
        self._tableModel.loadLayer()
        
        self._tableFilterModel = QgsAttributeTableFilterModel(iface.mapCanvas(), self._tableModel)
        self.setModel(self._tableFilterModel)
        self.show()
    
    def rewireFeatureLayer(self, oldLayer, newLayer):
        self._featureCache = QgsVectorLayerCache(newLayer, newLayer.featureCount())
        self._tableModel = QgsAttributeTableModel(self._featureCache)
        self._tableModel.loadLayer()
        
        self._tableFilterModel = QgsAttributeTableFilterModel(self.iface.mapCanvas(), self._tableModel)
        self.setModel(self._tableFilterModel)
        self.show()
    
    
    