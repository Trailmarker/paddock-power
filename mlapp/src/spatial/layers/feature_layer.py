# -*- coding: utf-8 -*-
from functools import cached_property
from qgis.PyQt.QtCore import QObject, pyqtSignal, pyqtSlot

from qgis.core import QgsFeature, QgsProject, QgsVectorLayer

from ...utils import qgsDebug, resolveStylePath, PLUGIN_NAME
from ..features.feature import Feature
from ..fields.timeframe import Timeframe
from .mixins.layer_mixin import LayerMixin
from .mixins.workspace_connection_mixin import WorkspaceConnectionMixin

class FeatureLayer(QgsVectorLayer, WorkspaceConnectionMixin, LayerMixin):

    # Emit this signal when a selected Feature is updated
    selectedFeaturesChanged = pyqtSignal(list)
    currentTimeframeChanged = pyqtSignal(Timeframe)

    featuresChanged = pyqtSignal(list)

    def __init__(self,
                 featureType,
                 path,
                 layerName,
                 providerLib,
                 styleName=None,
                 *args, **kwargs):
        f"""Create a new {PLUGIN_NAME} vector layer."""

        self.featureType = featureType

        self._workspace = None
        # Route changes to this layer *through* the Paddock Power
        # workspace so other objects can respond
        self._blockWorkspaceConnnection = False

        self._selectedFeature = None

        super().__init__(path, layerName, providerLib, *args, **kwargs)

        self.applyNamedStyle(styleName)
        self.addInBackground()
        self.selectionChanged.connect(lambda selection, *_: self.onLayerSelectionChanged(selection))

    def getSchema(self):
        """Return the Schema for this layer."""
        raise NotImplementedError

    def getWkbType(self):
        """Return the WKB type for this layer."""
        raise NotImplementedError

    @cached_property
    def typeName(self):
        """Return the FeatureLayer's type name."""
        return type(self).__name__

    def __repr__(self):
        """Return a string representation of the Field."""
        return f"{self.typeName}(name={self.name()})"

    def __str__(self):
        """Convert the Field to a string representation."""
        return repr(self)

    def applyNamedStyle(self, styleName):
        """Apply a style to the layer."""
        # Optionally apply a style to the layer
        if styleName:
            stylePath = resolveStylePath(styleName)
            self.loadNamedStyle(stylePath)
        self.triggerRepaint()

    # Feature interface
    def wrapFeature(self, feature):
        """Wrap a QgsFeature using the Feature type of this FeatureLayer."""
        assert (not feature) or isinstance(feature, QgsFeature)
        return self.featureType(self, feature)

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

    def countFeatures(self):
        """Get the number of Features in the layer."""
        return len([f for f in self.getFeatures()])

    @pyqtSlot(list)
    def onLayerSelectionChanged(self, selection):
        """Handle the QGIS layer selection changing."""
        qgsDebug(f"{self.typeName}.onLayerSelectionChanged({selection})")
        if self.connectedToWorkspace:
            self.workspace.onLayerSelectionChanged(self, selection)

    @pyqtSlot(list)
    def onSelectedFeaturesChanged(self, features):
        """Handle the selected feature changing."""
        feature = features[0] if features else None

        if not self.connectedToWorkspace:
            return

        self._blockWorkspaceConnnection = True

        try:
            # Was something selected?
            hadSelection = self._selectedFeature is not None
            qgsDebug(f"{self.__class__.__name__}.onSelectedFeaturesChanged: hadSelection={hadSelection}")

            # Is this our Feature?
            ourFeature = (
                feature is not None) and (
                feature.featureLayer is not None) and (
                self.id() == feature.featureLayer.id())
            qgsDebug(f"{self.__class__.__name__}.onSelectedFeaturesChanged: ourFeature={ourFeature}")

            # Are we going to focus based on this new Feature?
            focusOnSelect = feature and feature.focusOnSelect()
            qgsDebug(f"{self.__class__.__name__}.onSelectedFeaturesChanged: focusOnSelect={focusOnSelect}")

            # Is it the same one that's already selected?
            sameAsSelected = ourFeature and hadSelection and (self._selectedFeature.FID == feature.FID)
            qgsDebug(f"{self.__class__.__name__}.onSelectedFeaturesChanged: sameAsSelected={sameAsSelected}")

            # If this new feature has focusOnSelect, and it's not already selected,
            # clear our selection unless we're selecting the same Feature
            if hadSelection and focusOnSelect and (not ourFeature or not sameAsSelected):
                qgsDebug(f"{self.__class__.__name__}.onSelectedFeaturesChanged: clearing currently selected {self._selectedFeature}")
                self._selectedFeature.onDeselectFeature()
                self._selectedFeature = None

            if ourFeature:
                self.selectByIds([feature.id], QgsVectorLayer.SetSelection)

                if not sameAsSelected:
                    qgsDebug(f"{self.__class__.__name__}.onSelectedFeaturesChanged: selecting {feature}")
                    self._selectedFeature = feature
                    feature.onSelectFeature()
                    qgsDebug(f"{self.__class__.__name__}.onSelectedFeaturesChanged: selectedFeaturesChanged.emit(feature)")
                    self.selectedFeaturesChanged.emit([feature])
            elif focusOnSelect:
                qgsDebug(f"{self.__class__.__name__}.onSelectedFeaturesChanged: clearing QgsVectorLayer selection")
                self.removeSelection()
                qgsDebug(f"{self.__class__.__name__}.onSelectedFeaturesChanged: selectedFeaturesChanged.emit(None)")
                self.selectedFeaturesChanged.emit([])

        finally:
            self._blockWorkspaceConnnection = False
