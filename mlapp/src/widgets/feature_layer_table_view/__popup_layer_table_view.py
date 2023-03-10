# # -*- coding: utf-8 -*-
# from qgis.core import QgsProject

# from ...models import Glitch
# from ...utils import qgsDebug
# from ...layers.popup_layer_consumer_mixin import PopupLayerConsumerMixin
# from .feature_layer_table_view import FeatureLayerTableView


# class PopupLayerTableView(FeatureLayerTableView, PopupLayerConsumerMixin):
    
#     @property
#     def popupLayerType(self):
#         pass

#     def __init__(self, parent=None):
#         """Constructor."""
#         FeatureLayerTableView.__init__(self, parent)
#         PopupLayerConsumerMixin.__init__(self)

#     @property
#     def popupLayerTypes(self):
#         """Popup layer types that this layer can consume."""
#         return [self.popupLayerType]

#     @property
#     def popupLayer(self, layerType):
#         """Get the current popup layer of the given type."""
#         if layerType != self.popupLayerType:
#             raise Glitch("Unexpected layer type: %s" % layerType)
#         return self.featureLayer

#     def onPopupLayerAdded(self, layerId):
#         qgsDebug(f"{type(self).__name__}.onPopupLayerAdded({layerId})")
#         featureLayer = QgsProject.instance().mapLayer(layerId)

#         if type(featureLayer) in self.popupLayerTypes:
#             self.featureLayer = featureLayer
#             self.refreshList()

#     def onPopupLayerRemoved(self):
#         qgsDebug(f"{type(self).__name__}.onPopupLayerRemoved()")
#         self.featureLayer = None
#         self.refreshList()
