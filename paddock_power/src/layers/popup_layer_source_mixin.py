# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsProject

from .interfaces import IFeature, IFeatureLayer
from .popup_feature_layer import PopupFeatureLayer


class PopupLayerSourceMixin(IFeatureLayer):

    popupFeatureSelected = pyqtSignal(str)
    popupFeaturesDeselected = pyqtSignal()

    popupLayerAdded = pyqtSignal(str)
    popupLayerRemoved = pyqtSignal()

    def __init__(self):
        self.__popupLayers = {}

    @classmethod
    def __key(self, layerType):
        return layerType.__name__ if isinstance(layerType, type) else layerType

    def connectPopups(self):
        self.popupFeatureSelected.connect(lambda layerId: self.onSelectPopupFeature(layerId))
        self.popupFeaturesDeselected.connect(lambda: self.onPopupFeaturesDeselected())

        self.popupLayerAdded.connect(lambda id: self.onPopupLayerAdded(id))
        self.popupLayerRemoved.connect(lambda: self.onPopupLayerRemoved())

    def addPopupLayer(self, layerType, feature):
        """Add a popup layer."""
        if not feature:
            return

        assert issubclass(layerType, PopupFeatureLayer)
        assert isinstance(feature, IFeature)

        item = self.findItem()
        if not item:
            # This layer isn't in the map, don't create the popup
            return

        # Remove any existing popup layers of this type - they don't play nice together
        # layerType.removeAllOfType()

        popupLayer = layerType(feature)
        self.__popupLayers[self.__key(layerType)] = popupLayer.id()

        group = item.parent()
        layerIndex = group.children().index(item)

        # The relativeLayerPosition determines where a popup layer is inserted in the group
        group.insertLayer(max(0, layerIndex + self.relativeLayerPosition), popupLayer)

        self.popupLayerAdded.emit(popupLayer.id())

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
                    popupLayer.triggerRepaint(True)
                    node.parent().removeChildNode(node)
                    QgsProject.instance().removeMapLayer(popupLayer.id())
            except BaseException:
                pass
            finally:
                # self.popupLayerRemoved.emit()
                popupLayer = None

    def removeAllPopupLayers(self):
        """Remove all popup layers associated with this source."""
        layerIds = [self.__popupLayers[self.__key(layerType)] for layerType in self.__popupLayers]

        for layerId in layerIds:
            try:
                if layerId in QgsProject.instance().mapLayers():
                    self.removePopupLayer(QgsProject.instance().mapLayer(layerId))
            except BaseException:
                pass
            finally:
                self.popupLayerRemoved.emit()

    def onSelectPopupFeature(self, feature):
        """To be overridden and called when the popup layer source selects a popup feature."""
        self.addAllPopupLayers(feature)

    def onDeselectPopupFeatures(self):
        """To be overridden and called when the popup layer source deselects a popup feature."""
        self.removeAllPopupLayers()

    def onPopupLayerAdded(self, layerId):
        """To be overridden and called when the popup layer source adds a popup layer."""
        pass

    def onPopupLayerRemoved(self):
        """To be overridden and called when the popup layer source removes a popup layer."""
        pass
