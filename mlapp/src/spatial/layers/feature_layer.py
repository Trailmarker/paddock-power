# -*- coding: utf-8 -*-
from collections import namedtuple
from functools import cached_property

from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot

from qgis.core import QgsFeature, QgsVectorLayer

from ...utils import qgsDebug, resolveStylePath, PLUGIN_NAME
from ..fields.timeframe import Timeframe
from .mixins.layer_mixin import LayerMixin
from .mixins.interaction_mixin import InteractionMixin


class FeatureLayer(QgsVectorLayer, InteractionMixin, LayerMixin):

    # Emit this signal when a selected Feature is updated
    selectedFeatureChanged = pyqtSignal(type, int, bool)
    currentTimeframeChanged = pyqtSignal(Timeframe)

    def __init__(self,
                 featureType,
                 path,
                 layerName,
                 providerLib,
                 styleName=None,
                 *args, **kwargs):
        f"""Create a new {PLUGIN_NAME} vector layer."""

        self._featureType = featureType

        self._workspace = None
        # Route changes to this layer *through* the Paddock Power
        # workspace so other objects can respond
        self._blockWorkspaceConnnection = False

        self._selectedFeature = None

        super().__init__(path, layerName, providerLib, *args, **kwargs)

        self.applyNamedStyle(styleName)
        self.addInBackground()
        self.selectionChanged.connect(lambda selection, *_: self.onLayerSelectionChanged(selection))

    @property
    def featureType(self):
        return self._featureType

    def focusOnSelect(self):
        """Return True if this layer should be focused when a feature is selected."""
        return self.featureType.focusOnSelect()

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
        # qgsDebug(f"{self.typeName}.getFeaturesInCurrentTimeframe({self.currentTimeframe})")
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

   