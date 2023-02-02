# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsFeatureRequest, QgsVectorLayer

from ..models import QtAbstractMeta, WorkspaceMixin
from ..utils import qgsDebug, resolveStylePath, PLUGIN_NAME
from .interfaces import IFeatureLayer
from .map_layer_mixin import MapLayerMixin


class FeatureLayer(QgsVectorLayer, WorkspaceMixin, MapLayerMixin, IFeatureLayer, metaclass=QtAbstractMeta):

    featureSelected = pyqtSignal(type)
    featureDeselected = pyqtSignal(type)

    @classmethod
    def getFeatureType(cls):
        """Return the Feature type for this layer."""
        raise NotImplementedError

    @classmethod
    def getSchema(cls):
        """Return the Schema for this layer."""
        return cls.getFeatureType().getSchema()

    @classmethod
    def getWkbType(cls):
        """Return the WKB type for this layer."""
        return cls.getSchema().wkbType

    @classmethod
    def focusOnSelect(self):
        """Return True if this layer should be focused when a feature is selected."""
        return self.getFeatureType().focusOnSelect()

    def __init__(self,
                 path,
                 layerName,
                 providerLib,
                 styleName=None,
                 *args, **kwargs):
        f"""Create a new {PLUGIN_NAME} vector layer."""
        # Clear out any unwanted friends from the map … (classmethod defined in LayerMixin)
        # TODO - does not work
        # self.detectAndRemoveAllOfType()

        super().__init__(path, layerName, providerLib, *args, **kwargs)
        MapLayerMixin.__init__(self)
        WorkspaceMixin.__init__(self)

        self.applyNamedStyle(styleName)
        self.addInBackground()

        self.plugin.workspaceReady.connect(self.onWorkspaceReady)

    def onWorkspaceReady(self):
        self.selectionChanged.connect(self.onSelectionChanged)

        self.workspace.featureLayerSelected.connect(self.onFeatureLayerSelected)
        self.workspace.featureLayerDeselected.connect(self.onFeatureLayerDeselected)
        self.workspace.timeframeChanged.connect(self.onTimeframeChanged)

    @property
    def hasPopups(self):
        return False

    def __repr__(self):
        """Return a string representation of the Field."""
        return f"{type(self).__name__}(name={self.name()})"

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
        return self.getFeatureType()(self, feature)

    def _wrapFeatures(self, features):
        """Adapt the features in this layer."""
        for feature in features:
            feature = self.wrapFeature(feature)
            yield feature

    def getFeaturesByTimeframe(self, timeframe, request=None):
        """Get the features in this layer that are in the current timeframe."""
        features = self.getFeatures(request)
        return [f for f in features if f.matchTimeframe(timeframe)]

    def getFeaturesInCurrentTimeframe(self, request=None):
        """Get the features in this layer that are in the current timeframe."""
        features = self.getFeatures(request)
        return [f for f in features if f.matchTimeframe(self.timeframe)]

    def getFeature(self, id):
        """Get a feature by its id, assumed to be the same as its FID."""
        feature = super().getFeature(id)
        return self.wrapFeature(feature) if feature else None

    def getFeatureFromSelection(self, selectionId):
        """Convenience function as in rare cases this has to behave differently."""
        return self.getFeature(selectionId)

    def getFeatures(self, request=None):
        """Get the features in this layer."""
        if request is None:
            return self._wrapFeatures(super().getFeatures())

        return self._wrapFeatures(super().getFeatures(request))

    def countFeatures(self):
        """Get the number of Features in the layer."""
        return len([f for f in self.getFeatures()])

    def onFeatureLayerSelected(self, layerType):
        if isinstance(self, layerType):
            feature = self.workspace.selectedFeature(layerType)
            self.onSelectFeature(feature)
            self.featureSelected.emit(layerType)

    def onFeatureLayerDeselected(self, layerType):
        if isinstance(self, layerType):
            # self.removeSelection()
            self.onDeselectFeature()
            self.featureDeselected.emit(layerType)

    def onTimeframeChanged(self, timeframe):
        self.triggerRepaint()

    def onSelectFeature(self, feature):
        # qgsDebug(f"{type(self).__name__}.selectFeature({feature})")
        feature.zoomFeature()
        pass

    def onDeselectFeature(self):
        # qgsDebug(f"{type(self).__name__}.onDeselectFeature()")
        pass

    def onSelectionChanged(self, selection, *_):
        if len(selection) == 1:
            feature = next(self.getFeatures(QgsFeatureRequest().setFilterFids(selection)), None)
            if feature:
                self.workspace.selectFeature(feature)
