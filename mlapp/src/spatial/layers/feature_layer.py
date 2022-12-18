# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot

from qgis.core import QgsProject, QgsVectorLayer

from ...models.glitch import Glitch
from ...models.qt_abstract_meta import QtAbstractMeta
from ...utils import resolveStylePath, PLUGIN_NAME
from ..features.feature import Feature


class FeatureLayer(ABC, QgsVectorLayer, metaclass=QtAbstractMeta):

    # emit this signal when a selected Feature is updated
    selectedFeatureChanged = pyqtSignal(Feature)

    @abstractmethod
    def getFeatureType(self):
        """Return the type of feature that this layer contains. Override in subclasses"""
        pass

    def __init__(self, project, *args, **kwargs):
        f"""Create a new {PLUGIN_NAME} vector layer."""

        # Keep a reference to the Paddock Power Project
        assert(project is not None)
        self._project = project
        self._selectedFeature = None

        styleName = kwargs.pop("styleName", None)

        super().__init__(*args, **kwargs)

        # Optionally apply a style to the layer
        if styleName is not None:
            stylePath = resolveStylePath(styleName)
            self.loadNamedStyle(stylePath)

        # Route changes to this layer's selection *through* the Paddock Power
        # Project for *all* Paddock Power FeatureLayers
        self._project.selectedFeatureChanged.connect(self.onSelectedFeatureChanged)
        self.selectionChanged.connect(lambda selection, *_: self._project.onLayerSelectionChanged(self, selection))

    def detectAndRemove(self):
        """Detect if a layer is already in the map, and if so, remove it."""
        layers = [l for l in QgsProject.instance().mapLayers().values()]
        for layer in layers:
            if layer.source() == self.source():
                QgsProject.instance().removeMapLayer(layer.id())

    @classmethod
    def detectAndRemoveAllOfType(cls):
        """Detect if any layers of the same type are already in the map, and if so, remove them. Use with care."""
        layers = [l for l in QgsProject.instance().mapLayers().values() if type(l).__name__ == cls.__name__]
        for layer in layers:
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

    def getPaddockPowerProject(self):
        """Get the PaddockPowerProject for this layer."""
        return self._project

    def getFeature(self, fid):
        """Get a feature by its ID."""
        feature = super().getFeature(fid)
        return self.wrapFeature(feature) if feature else None

    def getFeatures(self, request=None):
        """Get the features in this layer."""
        if request is None:
            return self._wrapQgsFeatures(super().getFeatures())

        return self._wrapQgsFeatures(super().getFeatures(request))

    def featureCount(self):
        """Get the number of Features in the layer."""
        return len([f for f in self.getFeatures()])

    @pyqtSlot(Feature)
    def onSelectedFeatureChanged(self, selectedFeature):
        """Handle the selected feature changing."""

        if selectedFeature and selectedFeature.featureLayer and selectedFeature.featureLayer.id() == self.id():
            if self._selectedFeature and self._selectedFeature.id == selectedFeature.id:
                # Reselecting the same Feature, TODO?
                return
            self._selectedFeature = selectedFeature
            self._selectedFeature.onSelectFeature()
            self.selectedFeatureChanged.emit(self._selectedFeature)

        elif self._selectedFeature:
            self._selectedFeature.onDeselectFeature()
            self._selectedFeature = None
            self.selectedFeatureChanged.emit(self._selectedFeature)


