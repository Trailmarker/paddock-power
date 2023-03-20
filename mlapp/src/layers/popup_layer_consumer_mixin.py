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
            try:
                oldVal.popupLayerAdded.disconnect()
            except Exception:
                pass
            try:
                oldVal.popupLayerRemoved.disconnect()
            except Exception:
                pass
        if newVal:
            newVal.popupLayerAdded.connect(lambda layerId: self.onPopupLayerAdded(layerId))
            newVal.popupLayerRemoved.connect(lambda: self.onPopupLayerRemoved())

    def onPopupLayerAdded(self, layerId):
        """Override in subclass to handle popup layer added."""
        pass

    def onPopupLayerRemoved(self):
        """Override in subclass to handle popup layer removed."""
        pass
