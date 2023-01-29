# -*- coding: utf-8 -*-
from abc import abstractproperty

from qgis.core import QgsProject

from ...features.feature import Feature
from ..feature_layer import FeatureLayer
from .popup_feature_layer_mixin import PopupFeatureLayerMixin


class PopupFeatureMixin:

    def __init__(self):
        super().__init__()

        assert isinstance(self, Feature)
        assert isinstance(self.featureLayer, PopupFeatureLayerMixin)

        self.__popupLayers = {}

    @abstractproperty
    def popupLayerTypes(self):
        pass

    def __key(self, layerType):
        return layerType.__name__ if isinstance(layerType, type) else layerType

    def __val(self, layer):
        return layer if isinstance(layer, FeatureLayer) else QgsProject.instance().mapLayer(layer)

    def getPopupLayer(self, layerType):
        """Get the popup layer with the given name."""
        assert issubclass(layerType, FeatureLayer)
        return self.__popupLayers.get(self.__key(layerType), None)

    def addPopupLayer(self, layerType):
        """Add a Metrick Paddock popup layer."""
        assert issubclass(layerType, FeatureLayer)

        if not self.getPopupLayer(layerType):
            item = QgsProject.instance().layerTreeRoot().findLayer(self.featureLayer)
            if not item:
                # If this layer isn't in the map, don't initialise or add the Paddock Land Types layer.
                return

            # Remove any existing popup layers of this type - they don't play nice together
            layerType.detectAndRemoveAllOfType()

            popupLayer = layerType(self)
            self.__popupLayers[self.__key(layerType)] = popupLayer.id()

            # Bit of a hack but it looks nicer if it's above the derived Boundary layer …
            group = item.parent()
            group.insertLayer(max(0, group.children().index(item) - 1), popupLayer)

            self.featureLayer.popupLayerAdded.emit(self, popupLayer)

    def removePopupLayer(self, obj):
        """Remove any Metric Paddock popup layer."""

        popupLayer = obj if isinstance(obj, FeatureLayer) else self.__popupLayers.pop(self.__key(obj), None)

        if popupLayer:
            try:
                node = QgsProject.instance().layerTreeRoot().findLayer(popupLayer)
                if node:
                    node.setItemVisibilityChecked(False)
                    popupLayer.triggerRepaint()
                    node.parent().removeChildNode(node)
                    QgsProject.instance().removeMapLayer(popupLayer.id())
            except BaseException:
                pass
            finally:
                self.featureLayer.popupLayerRemoved.emit(self)
                self.popupLayer = None

    def removeAllPopupLayers(self):
        layerIds = [self.__popupLayers[self.__key(layerType)] for layerType in self.__popupLayers]

        for layerId in layerIds:
            if layerId in QgsProject.instance().mapLayers():
                self.removePopupLayer(QgsProject.instance().mapLayer(layerId))

    def onSelectFeature(self):
        """Do the stuff we'd normally do, but also add the Paddock Land Types popup layer."""
        super().onSelectFeature()
        for layerType in self.popupLayerTypes:
            self.addPopupLayer(layerType)

    def onDeselectFeature(self):
        """Do the stuff we'd normally do, but also remove the Paddock Land Types popup layer."""
        super().onDeselectFeature()
        self.removeAllPopupLayers()
