# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ...models import Glitch
from ...utils import qgsDebug
from ...layers.popup_layer_consumer_mixin import PopupLayerConsumerMixin
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

    @featureLayer.setter
    def featureLayer(self, value):
        """Set the FeatureLayer - override this."""
        self._featureLayer = value
        self.refreshList()

    def onPopupLayerAdded(self, layerId):
        qgsDebug(f"{type(self).__name__}.onPopupLayerAdded({layerId})")
        featureLayer = QgsProject.instance().mapLayer(layerId)

        if type(featureLayer) in self.popupLayerTypes:
            self._featureLayer = featureLayer
            self.refreshList()

    def onPopupLayerRemoved(self):
        qgsDebug(f"{type(self).__name__}.onPopupLayerRemoved()")
        self._featureLayer = None
        self.refreshList()
