# -*- coding: utf-8 -*-

from abc import abstractmethod
from ...utils import qgsDebug
from .feature_list_base import FeatureListBase


class FeatureLayerList(FeatureListBase):
    def __init__(self, listItemFactory, parent=None):
        """Constructor."""
        super().__init__(listItemFactory, parent)

        self._timeframe = self.workspace.timeframe
        self._timeframeOverride = False
        self.workspace.timeframeChanged.connect(self.refreshUi)

        self._featureLayer = None

        self.refreshUi()

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
        self.refreshUi()

    def rewireFeatureLayer(self, oldVal, newVal):
        """Rewire the FeatureLayer."""
        # qgsDebug(f"{type(self).__name__}.rewireFeatureLayer({oldVal}, {newVal})")
        if oldVal:
            oldVal.featureSelected.disconnect(self.changeSelection)
            oldVal.featureDeselected.disconnect(self.removeSelection)
        if newVal:
            newVal.featureSelected.connect(self.changeSelection)
            newVal.featureDeselected.connect(self.removeSelection)

    def getFeatures(self):
        """Get the Features."""
        if self.featureLayer:
            return [feature for feature in self.featureLayer.getFeaturesByTimeframe(self.timeframe)]
            # qgsDebug(f"{type(self).__name__}.getFeatures(): len(features) = {len(features)}")
        else:
            # qgsDebug(f"{type(self).__name__}.refreshUi(): featureLayer is None")
            return []
