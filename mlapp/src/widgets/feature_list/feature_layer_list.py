# -*- coding: utf-8 -*-

from ...utils import qgsDebug
from ...layers.fields import TIMEFRAME
from .feature_list_base import FeatureListBase

from qgis.core import QgsFeatureRequest, QgsVectorLayerCache


class FeatureLayerList(FeatureListBase):

    class FeatureCache(QgsVectorLayerCache):
        def __init__(self, layer, count):
            super().__init__(layer, count)

        def featureRemoved(self, fid):
            super().featureRemoved(fid)
            self.removeListItem(fid)

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
    def featureLayer(self, newLayer):
        [oldLayer, self._featureLayer] = [self._featureLayer, newLayer]
        self.rewireFeatureLayer(oldLayer, newLayer)

    def rewireFeatureLayer(self, oldLayer, newLayer):
        """Rewire the FeatureLayer."""
        # qgsDebug(f"{type(self).__name__}.rewireFeatureLayer({oldVal}, {newVal})")
        if oldLayer:
            oldLayer.layerTruncated.disconnect(self.clearAndRefreshCache)
            oldLayer.featuresUpserted.disconnect(self.refreshList)
            oldLayer.featuresDeleted.disconnect(self.refreshList)
            oldLayer.featuresBulkAdded.disconnect(self.clearAndRefreshCache)

            oldLayer.featureSelected.disconnect(self.changeSelection)
            oldLayer.featureDeselected.disconnect(self.removeSelection)

            if self._layerCache:
                del(self._layerCache)
                self._layerCache = None
        if newLayer:
            newLayer.layerTruncated.connect(self.clearAndRefreshCache)
            newLayer.featuresUpserted.connect(self.clearAndRefreshCache)
            newLayer.featuresDeleted.connect(self.removeListItems)
            newLayer.featuresBulkAdded.connect(self.clearAndRefreshCache)

            newLayer.featureSelected.connect(self.changeSelection)
            newLayer.featureDeselected.connect(self.removeSelection)
            self._layerCache = QgsVectorLayerCache(newLayer, newLayer.featureCount())

            self._layerCache.finished.connect(self.refreshList)
            self._layerCache.invalidated.connect(self.clearAndRefreshCache)
            self.clearAndRefreshCache()

    def listFeatures(self, request=None):
        """Get the items in the list."""
        # return self.getFeatures(request)
        return self.getFeaturesInCurrentTimeframe(request)

    def clearAndRefreshCache(self):
        """Refresh the cache."""
        qgsDebug(f"{type(self).__name__}.clearAndRefreshCache()")
        self.clear()
        if self._layerCache:
            self._layerCache.setFullCache(True)

    def removeListItems(self, fids):
        for fid in fids:
            self.removeListItem(fid)

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
