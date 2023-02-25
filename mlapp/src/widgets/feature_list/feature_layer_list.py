# -*- coding: utf-8 -*-

from ...layers.fields import TIMEFRAME
from .feature_list_base import FeatureListBase

from qgis.core import QgsFeatureRequest, QgsVectorLayerCache


class FeatureLayerList(FeatureListBase):
    def __init__(self, listItemFactory, parent=None):
        """Constructor."""
        super().__init__(listItemFactory, parent)

        self._timeframe = self.workspace.timeframe
        self._timeframeOverride = False
        self.workspace.timeframeChanged.connect(self.refreshList)

        self._featureLayer = None
        self._layerCache = None  # QgsVectorLayerCache(self._featureLayer, self._featureLayer.featureCount())

        # self.refreshList()

    @property
    def timeframe(self):
        if not self._timeframeOverride:
            return self.workspace.timeframe
        else:
            return self._timeframe

    @timeframe.setter
    def timeframe(self, timeframe):
        self._timeframe = timeframe
        self._timeframeOverride = True

    @property
    def featureLayer(self):
        """Get the FeatureLayer."""
        return self._featureLayer

    @featureLayer.setter
    def featureLayer(self, newVal):
        oldVal = self._featureLayer
        self._featureLayer = newVal
        self.rewireFeatureLayer(oldVal, newVal)

    def rewireFeatureLayer(self, oldLayer, newLayer):
        """Rewire the FeatureLayer."""
        # qgsDebug(f"{type(self).__name__}.rewireFeatureLayer({oldVal}, {newVal})")
        if oldLayer:
            oldLayer.featuresChanged.disconnect(self.refreshList)
            oldLayer.featureSelected.disconnect(self.changeSelection)
            oldLayer.featureDeselected.disconnect(self.removeSelection)
            if self._layerCache:
                del(self._layerCache)
        if newLayer:
            # newLayer.featuresChanged.connect(self.refreshList)
            newLayer.featureSelected.connect(self.changeSelection)
            newLayer.featureDeselected.connect(self.removeSelection)
            self._layerCache = QgsVectorLayerCache(newLayer, newLayer.featureCount())
            self._layerCache.cachedLayerDeleted.connect(self.clear)
            self._layerCache.attributeValueChanged.connect(lambda fid, *_: self.refreshListItem(fid))
            self._layerCache.featureAdded.connect(lambda fid, *_: self.refreshListItem(fid))
            self._layerCache.finished.connect(self.refreshList)
            self._layerCache.invalidated.connect(self.refreshCache)
            self.refreshCache()

    def listFeatures(self, request=None):
        """Get the items in the list."""
        return self.getFeaturesInCurrentTimeframe(request)

    def refreshCache(self):
        """Refresh the cache."""
        if self._layerCache:
            self._layerCache.setFullCache(True)

    def getFeatures(self, request=None):
        """Get the Features."""
        for feature in self._layerCache.getFeatures(request):
            yield self._featureLayer.wrapFeature(feature)

    def getFeaturesByTimeframe(self, timeframe, request=None):
        """Get the features in this layer that are in a specified timeframe."""
        request = request or QgsFeatureRequest()

        if self.featureLayer.getFeatureType().hasField(TIMEFRAME):
            request.setFilterExpression(timeframe.getFilterExpression())
            return self.getFeatures(request)
        else:
            features = self.getFeatures(request)
            return [f for f in features if f.matchTimeframe(timeframe)]

    def getFeaturesInCurrentTimeframe(self, request=None):
        """Get the features in this layer that are in the current timeframe."""
        return self.getFeaturesByTimeframe(self.featureLayer.timeframe, request)

    def getFeature(self, id):
        """Get a feature by its id, assumed to be the same as its FID."""
        feature = self._layerCache.getFeature(id)
        return self.featureLayer.wrapFeature(feature) if feature and feature.isValid() else None

    def getFeatureFromSelection(self, selectionId):
        """Convenience function as in rare cases this has to behave differently."""
        return self.getFeature(selectionId)

    def countFeatures(self):
        """Get the number of Features in the layer."""
        return len([f for f in self.getFeatures()])
