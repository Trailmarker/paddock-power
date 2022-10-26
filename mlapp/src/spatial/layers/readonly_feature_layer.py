# -*- coding: utf-8 -*-
from abc import ABC, abstractclassmethod
from qgis.core import QgsProject, QgsVectorLayer

from ...models.glitch import Glitch
from ...models.qt_abstract_meta import QtAbstractMeta
from ...utils import resolveStylePath


class ReadOnlyFeatureLayer(ABC, QgsVectorLayer, metaclass=QtAbstractMeta):

    @abstractclassmethod
    def getFeatureType(cls):
        """Return the type of feature that this layer contains. Override in subclasses"""
        pass

    def __init__(self, *args, **kwargs):
        """Create a new Paddock Power vector layer."""

        styleName = kwargs.pop("styleName", None)

        super().__init__(*args, **kwargs)

        # Optionally apply a style to the layer
        if styleName is not None:
            stylePath = resolveStylePath(styleName)
            self.loadNamedStyle(stylePath)

        self.detectAndRemove()
        QgsProject.instance().addMapLayer(self, False)

    def detectAndRemove(self):
        """Detect if a layer is already in the map, and if so, return it."""
        layers = [l for l in QgsProject.instance().mapLayers().values()]
        for layer in layers:
            if layer.source() == self.source():
                QgsProject.instance().removeMapLayer(layer.id())

    def wrapFeature(self, feature):
        return self.getFeatureType()(self, feature)

    def addToMap(self, group):
        """Ensure the layer is in the map in the target group, adding it if necessary."""
        if group is None:
            raise Glitch(
                "FeatureLayer.addToMap: the layer group is not present")

        group.addLayer(self)

    def removeFromMap(self, group):
        node = group.findLayer(self.id())
        if node:
            group.removeChildNode(node)

    def setVisible(self, group, visible):
        """Set the layer's visibility."""
        node = group.findLayer(self.id())
        if node:
            node.setItemVisibilityChecked(visible)

    def _unwrapQgsFeature(self, feature):
        """Unwrap a Feature into a QgsFeature."""
        if not isinstance(feature, self.getFeatureType()):
            raise Glitch(
                f"FeatureLayer.__unwrapQgsFeature: the feature is not a {self.getFeatureType().__name__}")
        return feature._qgsFeature

    def _wrapQgsFeatures(self, qgsFeatures):
        """Adapt the features in this layer."""
        for feature in qgsFeatures:
            feature = self.wrapFeature(feature)
            yield feature

    def getFeatures(self, request=None):
        """Get the features in this layer."""
        if request is None:
            return self._wrapQgsFeatures(super().getFeatures())

        return self._wrapQgsFeatures(super().getFeatures(request))

    def featureCount(self):
        """Get the number of Features in the layer."""
        return len([f for f in self.getFeatures()])
