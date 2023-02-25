# -*- coding: utf-8 -*-

from ...models import Glitch
from ...layers.popup_layer_consumer_mixin import PopupLayerConsumerMixin
from ...utils import qgsDebug
from .feature_layer_list import FeatureLayerList


class PopupLayerList(FeatureLayerList, PopupLayerConsumerMixin):
    """Use the PopupLayerConsumeMixin to do a better job of handling change in
    lists of features that belong to rapidly changing popup layers."""

    @property
    def popupLayerType(self):
        pass

    def __init__(self, listItemFactory, parent=None):
        """Constructor."""
        FeatureLayerList.__init__(self, listItemFactory, parent)
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
        return self._featureLayer

    @property
    def featureLayer(self):
        """Get the FeatureLayer - override this."""
        return self._featureLayer

    def onPopupLayerAdded(self, layer):
        self._featureLayer = layer
        self.refreshList()

    def onPopupLayerRemoved(self):
        self._featureLayer = None
