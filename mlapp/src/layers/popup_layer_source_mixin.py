# -*- coding: utf-8 -*-
from abc import abstractmethod
from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsProject

from .interfaces import IFeature, IMapLayer
from .popup_feature_layer import PopupFeatureLayer


class PopupLayerSourceMixin(IMapLayer):

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

    @property
    @abstractmethod
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
        return layerType.__name__ if isinstance(layerType, type) else layerType

    def getPopupLayer(self, layerType):
        """Get the popup layer with the given name."""
        assert issubclass(layerType, PopupFeatureLayer)
        return self.__popupLayers.get(self.__key(layerType), None)

    def addPopupLayer(self, layerType, feature):
        """Add a Metric Paddock popup layer."""
        assert issubclass(layerType, PopupFeatureLayer)
        assert isinstance(feature, IFeature)

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

        # The relativeLayerPosition determines where a popup layer is inserted in the group
        group.insertLayer(max(0, layerIndex + self.relativeLayerPosition), popupLayer)

        self.popupLayerAdded.emit(popupLayer)

    def addAllPopupLayers(self, feature):
        for layerType in self.popupLayerTypes:
            self.addPopupLayer(layerType, feature)

    def removePopupLayer(self, obj):
        """Remove any current popup layer."""

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
                self.popupLayerRemoved.emit()
                self.popupLayer = None

    def removeAllPopupLayers(self):
        """Remove all popup layers associated with this source."""
        layerIds = [self.__popupLayers[self.__key(layerType)] for layerType in self.__popupLayers]

        for layerId in layerIds:
            if layerId in QgsProject.instance().mapLayers():
                self.removePopupLayer(QgsProject.instance().mapLayer(layerId))

    def onPopupFeatureSelected(self, layerType):
        """To be overridden and called when the popup layer source selects a popup feature."""
        feature = self.workspace.selectedFeature(layerType)
        self.addAllPopupLayers(feature)

    def onPopupFeatureDeselected(self, layerType):
        """To be overridden and called when the popup layer source deselects a popup feature."""
        self.removeAllPopupLayers()

    def onPopupLayerAdded(self, layer):
        """To be overridden and called when the popup layer source adds a popup layer."""
        pass

    def onPopupLayerRemoved(self):
        """To be overridden and called when the popup layer source removes a popup layer."""
        pass
