# -*- coding: utf-8 -*-
from abc import ABC
from functools import cached_property

from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot

from qgis.core import QgsFeature, QgsProject, QgsVectorLayer

from ...models.glitch import Glitch
from ...models.qt_abstract_meta import QtAbstractMeta
from ...utils import qgsDebug, qgsError, resolveStylePath, PLUGIN_NAME
from ..features.feature import Feature
from ..fields.timeframe import Timeframe


class FeatureLayer(ABC, QgsVectorLayer, metaclass=QtAbstractMeta):

    # emit this signal when a selected Feature is updated
    currentTimeframeChanged = pyqtSignal(Timeframe)
    selectedFeatureChanged = pyqtSignal(Feature)
    workspaceConnectionChanged = pyqtSignal()

    def __init__(self, featureType, *args, **kwargs):
        f"""Create a new {PLUGIN_NAME} vector layer."""

        self.featureType = featureType
        self._selectedFeature = None
        self._workspace = None

        # Route changes to this layer's selection *through* the Paddock Power
        # Workspace for *all* Paddock Power FeatureLayers
        self._blockWorkspaceConnnection = False

        self._styleName = kwargs.pop("styleName", None)

        super().__init__(*args, **kwargs)

        # Optionally apply a style to the layer
        if self._styleName is not None:
            stylePath = resolveStylePath(self._styleName)
            self.loadNamedStyle(stylePath)

        self.selectionChanged.connect(lambda selection, *_: self.onLayerSelectionChanged(selection))

    def getSchema(self):
        """Return the Schema for this layer."""
        return self.featureType.getSchema()
  
    def getWkbType(self):
        """Return the WKB type for this layer."""
        return self.featureType.getWkbType()
        
    @cached_property
    def _typeName(self):
        """Return the FeatureLayer's type name."""
        return type(self).__name__

    def __repr__(self):
        """Return a string representation of the Field."""
        return f"{self._typeName}(name={self.name()})"

    def __str__(self):
        """Convert the Field to a string representation."""
        return repr(self)

    @property
    def styleName(self):
        """Return the name of the style applied to this layer."""
        return self._styleName

    def connectWorkspace(self, workspace):
        self._workspace = workspace
        self.workspaceConnectionChanged.emit()

    @property
    def connectedToWorkspace(self):
        return self._workspace and not self._blockWorkspaceConnnection

    @property
    def workspace(self):
        return self._workspace

    # def detectAndRemove(self):
    #     """Detect if a layer is already in the map, and if so, remove it."""
    #     layers = [l for l in QgsProject.instance().mapLayers().values()]
    #     for layer in layers:
    #         if layer.source() == self.source():
    #             QgsProject.instance().removeMapLayer(layer.id())

    @classmethod
    def detectAndRemoveAllOfType(cls):
        """Detect if any layers of the same type are already in the map, and if so, remove them. Use with care."""
        layers = [l for l in QgsProject.instance().mapLayers().values() if type(l).__name__ == cls.__name__]
        for layer in layers:
            QgsProject.instance().removeMapLayer(layer.id())

    @property
    def currentTimeframe(self):
        """Get the current timeframe for this layer (same as that of the workspace)."""
        return self.workspace.currentTimeframe if self.connectedToWorkspace else Timeframe.Undefined

    def depend(self, layerType):
        """Get a layer we depend on to work with by type."""
        if self.connectedToWorkspace:
            return self.workspace.workspaceLayers.getLayer(layerType)
        else:
            qgsError(f"{self._typeName}.depend({layerType}): no workspace connection")
            
    def depends(self, *layerTypes):
        """Get a collection of layers we depend on to work with by their types."""
        return list(self.depend(layerType) for layerType in layerTypes)

    def setCurrentTimeframe(self, timeframe):
        """Set the current timeframe for this layer. This will also set the current timeframe for the workspace."""
        if self.connectedToWorkspace:
            self.workspace.setCurrentTimeframe(timeframe)

    def wrapFeature(self, feature):
        """Wrap a QgsFeature using the Feature type of this FeatureLayer."""
        assert isinstance(feature, QgsFeature)
        return self.featureType(self, feature)

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
    
    def _wrapFeatures(self, features):
        """Adapt the features in this layer."""
        for feature in features:
            feature = self.wrapFeature(feature)
            yield feature

    def getFeaturesInCurrentTimeframe(self, request=None):
        """Get the features in this layer that are in the current timeframe."""
        features = self.getFeatures(request)
        # qgsDebug(f"{self.__class__.__name__}.getFeaturesInCurrentTimeframe({self.currentTimeframe})")
        return [f for f in features if f.matchTimeframe(self.currentTimeframe)]

    def getFeature(self, fid):
        """Get a feature by its ID."""
        feature = super().getFeature(fid)
        return self.wrapFeature(feature) if feature else None

    def getFeatures(self, request=None):
        """Get the features in this layer."""
        if request is None:
            return self._wrapFeatures(super().getFeatures())

        return self._wrapFeatures(super().getFeatures(request))

    def featureCount(self):
        """Get the number of Features in the layer."""
        return len([f for f in self.getFeatures()])

    @pyqtSlot(list)
    def onLayerSelectionChanged(self, selection):
        """Handle the QGIS layer selection changing."""
        # qgsDebug(f"{self.__class__.__name__}.onLayerSelectionChanged({selection})")
        if self.connectedToWorkspace:
            self.workspace.onLayerSelectionChanged(self, selection)

    @pyqtSlot(Feature)
    def onSelectedFeatureChanged(self, feature):
        """Handle the selected feature changing."""

        if not self.connectedToWorkspace:
            return

        self._blockWorkspaceConnnection = True

        try:
            # Was something selected?
            hadSelection = self._selectedFeature is not None
            # qgsDebug(f"{self.__class__.__name__}.onSelectedFeatureChanged: hadSelection={hadSelection}")

            # Is this our Feature?
            ourFeature = (
                feature is not None) and (
                feature.featureLayer is not None) and (
                self.id() == feature.featureLayer.id())
            # qgsDebug(f"{self.__class__.__name__}.onSelectedFeatureChanged: ourFeature={ourFeature}")

            # Are we going to focus based on this new Feature?
            focusOnSelect = feature and feature.focusOnSelect()
            # qgsDebug(f"{self.__class__.__name__}.onSelectedFeatureChanged: focusOnSelect={focusOnSelect}")

            # Is it the same one that's already selected?
            sameAsSelected = ourFeature and hadSelection and (self._selectedFeature.FID == feature.FID)
            # qgsDebug(f"{self.__class__.__name__}.onSelectedFeatureChanged: sameAsSelected={sameAsSelected}")

            # If this new feature has focusOnSelect, and it's not already selected,
            # clear our selection unless we're selecting the same Feature
            if hadSelection and focusOnSelect and (not ourFeature or not sameAsSelected):
                # qgsDebug(f"{self.__class__.__name__}.onSelectedFeatureChanged: clearing currently selected {self._selectedFeature}")
                self._selectedFeature.onDeselectFeature()
                self._selectedFeature = None

            if ourFeature:
                self.selectByIds([feature.id], QgsVectorLayer.SetSelection)

                if not sameAsSelected:
                    # qgsDebug(f"{self.__class__.__name__}.onSelectedFeatureChanged: selecting {feature}")
                    self._selectedFeature = feature
                    feature.onSelectFeature()
                    # qgsDebug(f"{self.__class__.__name__}.onSelectedFeatureChanged: selectedFeatureChanged.emit(feature)")
                    self.selectedFeatureChanged.emit(feature)
            elif focusOnSelect:
                # qgsDebug(f"{self.__class__.__name__}.onSelectedFeatureChanged: clearing QgsVectorLayer selection")
                self.removeSelection()
                # qgsDebug(f"{self.__class__.__name__}.onSelectedFeatureChanged: selectedFeatureChanged.emit(None)")
                self.selectedFeatureChanged.emit(None)

        finally:
            self._blockWorkspaceConnnection = False


    @pyqtSlot(Timeframe)
    def onCurrentTimeframeChanged(self, timeframe):
        """Handle the current timeframe changing."""
        self.triggerRepaint(deferredUpdate=False)
        self.currentTimeframeChanged.emit(timeframe)

    @pyqtSlot()
    def onWorkspaceConnectionChanged(self):
        """Handle the workspace changing."""

        if self.workspace:
            self.workspace.selectedFeatureChanged.connect(self.onSelectedFeatureChanged)
            self.workspace.currentTimeframeChanged.connect(self.onCurrentTimeframeChanged)
            self.currentTimeframeChanged.connect(self.workspace.setCurrentTimeframe)
      
            qgsDebug(f"{self.__class__.__name__}.onWorkspaceConnectionChanged: adding map layer")
            QgsProject.instance().addMapLayer(self, False)
            
      
    
