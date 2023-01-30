# -*- coding: utf-8 -*-
from abc import abstractproperty
from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsProject

from ....utils import qgsDebug
from ...features.feature import Feature
from ..popup_feature_layer import PopupFeatureLayer


class PopupFeatureLayerMixin:

    popupLayerAdded = pyqtSignal(PopupFeatureLayer)
    popupLayerRemoved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.__popupLayers = {}
        self.popupLayerAdded.connect(self.onPopupLayerAdded)
        self.popupLayerRemoved.connect(self.onPopupLayerRemoved)

        self.featureSelected.connect(self.onPopupFeatureSelected)
        self.featureDeselected.connect(self.onPopupFeatureDeselected)

    @property
    def hasPopups(self):
        return True

    @abstractproperty
    def popupLayerTypes(self):
        pass

    @property
    def relativeLayerPosition(self):
        """Determines where this layer will be placed in relation to the 'host' FeatureLayer. As per other QGIS
           innovations, a positive number means it is *below* the host FeatureLayer in the stack—negative is above."""
        return 1

    @property
    def zoomPopupLayerOnLoad(self):
        """Self-explanatory."""
        return False

    @classmethod
    def __key(self, layerType):
        return layerType.__name__

    def getPopupLayer(self, layerType):
        """Get the popup layer with the given name."""
        assert issubclass(layerType, PopupFeatureLayer)
        return self.__popupLayers.get(self.__key(layerType), None)

    def addPopupLayer(self, layerType, feature):
        """Add a Metrick Paddock popup layer."""
        qgsDebug(f"{type(self).__name__}|PopupFeatureLayerMixin.addPopupLayer({layerType.__name__}, {feature})")
        assert issubclass(layerType, PopupFeatureLayer)
        assert isinstance(feature, Feature)


        item = self.findItem()
        if not item:
            # This layer isn't in the map, don't create the popup
            return

        # Remove any existing popup layers of this type - they don't play nice together
        layerType.detectAndRemoveAllOfType()

        popupLayer = layerType(feature)
        self.__popupLayers[self.__key(layerType)] = popupLayer.id()

        group = item.parent()
        layerIndex = group.children().index(item)

        # The "relativeLayerPosition determines whether a layer is below or above"
        group.insertLayer(max(0, layerIndex + self.relativeLayerPosition), popupLayer)
        
        if self.zoomPopupLayerOnLoad:
            popupLayer.zoomLayer()
        self.popupLayerAdded.emit(popupLayer)

    def addAllPopupLayers(self, feature):
        qgsDebug(f"{type(self).__name__}|PopupFeatureLayerMixin.addAllPopupLayers({feature}, self.popupLayerTypes={self.popupLayerTypes})")
        for layerType in self.popupLayerTypes:
            self.addPopupLayer(layerType, feature)

    def removePopupLayer(self, obj):
        """Remove any Metric Paddock popup layer."""

        popupLayer = obj if isinstance(obj, PopupFeatureLayer) else self.__popupLayers.pop(self.__key(obj), None)

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
                self.popupLayerRemoved.emit(self)
                self.popupLayer = None

    def removeAllPopupLayers(self):
        layerIds = [self.__popupLayers[self.__key(layerType)] for layerType in self.__popupLayers]

        for layerId in layerIds:
            if layerId in QgsProject.instance().mapLayers():
                self.removePopupLayer(QgsProject.instance().mapLayer(layerId))

    def onPopupFeatureSelected(self, layerType):
        qgsDebug(f"{type(self).__name__}|PopupFeatureLayerMixin.onPopupFeatureSelected({layerType.__name__})")

        feature = self.workspace.selectedFeature(layerType)
        self.addAllPopupLayers(feature)

    def onPopupFeatureDeselected(self, layerType):
        qgsDebug(f"{type(self).__name__}|PopupFeatureLayerMixin.onPopupFeatureDeselected({layerType.__name__})")

        self.removeAllPopupLayers()

    def onPopupLayerAdded(self, layer):
        qgsDebug(f"{type(self).__name__}|PopupFeatureLayerMixin.onPopupLayerAdded({layer.name()})")

    def onPopupLayerRemoved(self):
        qgsDebug(f"{type(self).__name__}|PopupFeatureLayerMixin.onPopupLayerRemoved()")
