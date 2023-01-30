# -*- coding: utf-8 -*-

from .feature_list_base import FeatureListBase

class FeatureLayerList(FeatureListBase):
    def __init__(self, listItemFactory, parent=None):
        """Constructor."""
        super().__init__(listItemFactory, parent)
        
        self._timeframe = self.workspace.timeframe
        self._timeframeOverride = False
        self.workspace.timeframeChanged.connect(self.refreshUi)
        
        if self.featureLayer:
            self.rewireFeatureLayer(None, self.featureLayer)
        
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
        """Set the FeatureLayer."""
        [self._featureLayer, oldVal] = [newVal, self._featureLayer]
        self.rewireFeatureLayer(oldVal, newVal)

    def rewireFeatureLayer(self, oldVal, newVal):
        """Rewire the FeatureLayer."""
        if oldVal:
            oldVal.featureSelected.disconnect(self.changeSelection)
            oldVal.featureDeselected.disconnect(self.removeSelection)
        if newVal:
            newVal.featureSelected.connect(self.changeSelection)
            newVal.featureDeselected.connect(self.removeSelection)


    def getFeatures(self):
        """Get the Features."""
        if self.featureLayer:
            # return [feature for feature in self.featureLayer.getFeatures()]
            return [feature for feature in self.featureLayer.getFeaturesByTimeframe(self.timeframe)]
        else:
            return []



     
