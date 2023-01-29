# -*- coding: utf-8 -*-
from abc import abstractproperty

from qgis.core import QgsProject

from ....utils import qgsDebug
from ...features.feature import Feature
from ..feature_layer import FeatureLayer


class PopupFeatureMixin:

    def __init__(self):
        super().__init__()

        assert isinstance(self, Feature)

        self.__popupLayers = {}

    @abstractproperty
    def popupLayerTypes(self):
        pass

    @property
    def relativeLayerPosition(self):
        """Determines where this layer will be placed in relation to the 'host' FeatureLayer. As per other QGIS
           innovations, a positive number means it is *below* the host FeatureLayer in the stack—negative is above."""
        return 1

    def __key(self, layerType):
        return layerType.__name__ if isinstance(layerType, type) else layerType

    def getPopupLayer(self, layerType):
        """Get the popup layer with the given name."""
        assert issubclass(layerType, FeatureLayer)
        return self.__popupLayers.get(self.__key(layerType), None)

    def addPopupLayer(self, layerType):
        """Add a Metrick Paddock popup layer."""
        assert issubclass(layerType, FeatureLayer)

        if not self.getPopupLayer(layerType):
            item = self.featureLayer.findItem()
            if not item:
                # This layer isn't in the map, don't create the popup
                return
            
            # Remove any existing popup layers of this type - they don't play nice together
            layerType.detectAndRemoveAllOfType()

            popupLayer = layerType(self)
            self.__popupLayers[self.__key(layerType)] = popupLayer.id()

            group = item.parent()
            layerIndex = group.children().index(item)

            # The "relativeLayerPosition determines whether a layer is below or above"
            group.insertLayer(max(0, layerIndex + self.relativeLayerPosition), popupLayer)

            self.featureLayer.popupLayerAdded.emit(popupLayer)

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

    # def onSelectFeature(self):
    #     """Do the stuff we'd normally do, but also add the popup layers."""
    #     super().onSelectFeature()
        
    #     qgsDebug(f"PopupFeatureMixin.onSelectFeature() - adding popup layers for {self}")
    #     for layerType in self.popupLayerTypes:
    #         self.addPopupLayer(layerType)

    # def onDeselectFeature(self):
    #     """Do the stuff we'd normally do, but also remove the popup layers."""
    #     super().onDeselectFeature()
    #     qgsDebug(f"PopupFeatureMixin.onSelectFeature() - removing popup layers for {self}")

    #     self.removeAllPopupLayers()
