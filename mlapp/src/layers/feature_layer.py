# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import pyqtSignal

from qgis.core import QgsFeatureRequest, QgsVectorLayer

from ..models import QtAbstractMeta, WorkspaceMixin
from ..utils import qgsDebug, resolveStylePath, PLUGIN_NAME
from .features import Edits
from .fields import TIMEFRAME
from .interfaces import IFeatureLayer
from .map_layer_mixin import MapLayerMixin


class FeatureLayer(QgsVectorLayer, WorkspaceMixin, MapLayerMixin, IFeatureLayer, metaclass=QtAbstractMeta):

    editsPersisted = pyqtSignal()

    featureSelected = pyqtSignal(str)
    featureDeselected = pyqtSignal(str)

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

        super().__init__(path, layerName, providerLib, *args, **kwargs)
        MapLayerMixin.__init__(self)
        WorkspaceMixin.__init__(self)

        self.applyNamedStyle(styleName)

    def __repr__(self):
        """Return a string representation of the Field."""
        return f"{type(self).__name__}(name={self.name()})"

    def __str__(self):
        """Convert the Field to a string representation."""
        return repr(self)

    def connectWorkspace(self, workspace):
        self.workspace = workspace

        self.selectionChanged.connect(lambda selection, *_: self.onSelectionChanged(selection, *_))
        self.workspace.timeframeChanged.connect(lambda timeframe: self.onTimeframeChanged(timeframe))
        self.editsPersisted.connect(self.onEditsPersisted)

    @property
    def hasPopups(self):
        return False

    def sameId(self, layerId):
        return self.id() == layerId

    # Feature interface
    def wrapFeature(self, feature):
        """Wrap a QgsFeature using the Feature type of this FeatureLayer."""
        return self.getFeatureType()(self, feature)

    def _wrapFeatures(self, features):
        """Adapt the features in this layer."""
        for feature in features:
            feature = self.wrapFeature(feature)
            yield feature

    def getFeatures(self, request=None):
        """Get the features in this layer."""
        if request is None:
            return self._wrapFeatures(super().getFeatures())

        return self._wrapFeatures(super().getFeatures(request))

    def getFeaturesByTimeframe(self, timeframe, request=None):
        """Get the features in this layer that are in a specified timeframe."""
        request = request or QgsFeatureRequest()

        if self.getFeatureType().hasField(TIMEFRAME):
            request.setFilterExpression(timeframe.getFilterExpression())
            return self.getFeatures(request)
        else:
            features = self.getFeatures(request)
            return [f for f in features if f.matchTimeframe(timeframe)]

    def getFeaturesInCurrentTimeframe(self, request=None):
        """Get the features in this layer that are in the current timeframe."""
        return self.getFeaturesByTimeframe(self.timeframe, request)

    def getFeature(self, id):
        """Get a feature by its id, assumed to be the same as its FID."""
        feature = super().getFeature(id)
        # Note the use of QgsFeature.isValid() here, an actual object is still
        # returned even when the id doesn't hit …
        return self.wrapFeature(feature) if feature.isValid() else None

    def getFeatureFromSelection(self, selectionId):
        """Convenience function as in rare cases this has to behave differently."""
        return self.getFeature(selectionId)

    def countFeatures(self):
        """Get the number of Features in the layer."""
        return len([f for f in self.getFeatures()])

    def onTimeframeChanged(self, timeframe):
        """Handle workspace timeframe changes."""
        self.triggerRepaint(True)

    def onEditsPersisted(self):
        """Handle a batch of edits being persisted on the underyling layer."""
        # At the moment, we just invalidate the cache and reload the layer
        self.triggerRepaint(True)

    def onSelectFeature(self, feature):
        qgsDebug(f"{type(self).__name__}.onSelectFeature({feature})")
        feature.zoomFeature()
        self.featureSelected.emit(self.id())
        
        if self.hasPopups:
            self.onSelectPopupFeature(feature)

    def onDeselectFeatures(self, fids):
        qgsDebug(f"{type(self).__name__}.onDeselectFeatures({[str(f) for f in fids]})")
        self.featureDeselected.emit(self.id())
        
        qgsDebug(f"{type(self).__name__}.onDeselectFeatures({[str(f) for f in fids]}) - featureDeselected emitted")
        if self.hasPopups:
            qgsDebug(f"{type(self).__name__}.onDeselectFeatures({[str(f) for f in fids]}) - calling onDeselectPopupFeatures")
            self.onDeselectPopupFeatures()
            qgsDebug(f"{type(self).__name__}.onDeselectFeatures({[str(f) for f in fids]}) - called onDeselectPopupFeatures")
            

    def onSelectionChanged(self, selection, deselection, *_):
        """Translate our own selectionChanged signal into a workspace selectFeature call."""
        qgsDebug(f"{type(self).__name__}.onSelectionChanged({selection}, {deselection}, {[str(s) for s in _]})")

        self.onDeselectFeatures(deselection)

        if len(selection) == 1:
            feature = next(self.getFeatures(QgsFeatureRequest().setFilterFids(selection)), None)
            if feature:
                self.onSelectFeature(feature)
                self.workspace.selectFeature(feature)
        
        
