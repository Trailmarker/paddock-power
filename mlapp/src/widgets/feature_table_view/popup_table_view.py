# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ...models import Glitch
from ...utils import qgsDebug
from ...layers.popup_layer_consumer_mixin import PopupLayerConsumerMixin
from .feature_table_view import FeatureTableView


class PopupTableView(FeatureTableView, PopupLayerConsumerMixin):
    """Use the PopupLayerConsumeMixin to do a better job of handling change in
    lists of features that belong to rapidly changing popup layers."""

    @property
    def popupLayerType(self):
        pass

    def __init__(self, schema, detailsWidgetFactory=None, editWidgetFactory=None, parent=None):
        """Constructor."""
        FeatureTableView.__init__(self, schema, detailsWidgetFactory, editWidgetFactory, parent)
        PopupLayerConsumerMixin.__init__(self)

    @property
    def popupLayerTypes(self):
        """Popup layer types that this layer can consume."""
        return [self.popupLayerType]

    @property
    def popupLayer(self, layerType):
        """Get the current popup layer of the given type."""
        if layerType != self.popupLayerType:
            raise Glitch("Unexpected layer type: %s" % layerType)
        return self.featureLayer

    def onPopupLayerAdded(self, layerId):
        featureLayer = QgsProject.instance().mapLayer(layerId)

        if type(featureLayer) in self.popupLayerTypes:
            qgsDebug(f"{type(self).__name__}.onPopupLayerAdded({layerId}) - would add")
        #     self.featureLayer = featureLayer

    def onPopupLayerRemoved(self):
        qgsDebug(f"{type(self).__name__}.onPopupLayerRemoved()")
        # self.featureLayer = None
        # pass
