# -*- coding: utf-8 -*-
from abc import abstractmethod


class PopupLayerConsumerMixin:

    def __init__(self):
        super().__init__()
        self._source = None
        self.__popupLayers = {}

    @property
    @abstractmethod
    def popupLayerTypes(self):
        """Popup layer types that this layer can consume."""
        pass

    def popupLayer(self, layerType):
        """Get the current popup layer of the given type."""
        return self.__popupLayers.get(layerType.id(), None)

    @property
    def popupLayerSource(self):
        return self._source

    @popupLayerSource.setter
    def popupLayerSource(self, newVal):
        """Set the source of popups."""
        oldVal = self._source
        self._source = newVal
        self.rewirePopupLayerSource(oldVal, newVal)

    def rewirePopupLayerSource(self, oldVal, newVal):
        """Rewire the PopupLayerSource."""
        if oldVal:
            oldVal.popupLayerAdded.disconnect(self.onPopupLayerAdded)
            oldVal.popupLayerRemoved.disconnect(self.onPopupLayerRemoved)
        if newVal:
            newVal.popupLayerAdded.connect(self.onPopupLayerAdded)
            newVal.popupLayerRemoved.connect(self.onPopupLayerRemoved)
