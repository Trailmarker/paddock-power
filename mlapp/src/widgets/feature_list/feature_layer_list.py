# -*- coding: utf-8 -*-
from qgis.core import QgsProject

from ...spatial.layers.mixins.popup_feature_layer_mixin import PopupFeatureLayerMixin
from .feature_list_base import FeatureListBase


class FeatureLayerList(FeatureListBase, PopupFeatureLayerMixin):
    def __init__(self, listItemFactory, parent=None):
        """Constructor."""
        self._featureLayerId = None
        super().__init__(listItemFactory, parent)
        self.refreshUi()

    @property
    def featureLayer(self):
        """Get the FeatureLayer."""
        return QgsProject.instance().mapLayer(self._featureLayerId) if self._featureLayerId else None


    def setFeatureLayer(self, featureLayer):
        """Set the FeatureLayer."""
        if self.featureLayer and isinstance(featureLayer, PopupFeatureLayerMixin):
            featureLayer.popupLayerAdded.disconnect(self.onPopupLayerAdded)
            featureLayer.popupLayerRemoved.disconnect(self.onPopupLayerRemoved)

        if featureLayer:
            self._featureLayerId = featureLayer.id()
            self.connectWorkspace(featureLayer.workspace)
            if isinstance(featureLayer, PopupFeatureLayerMixin):
                featureLayer.popupLayerAdded.connect(self.onPopupLayerAdded)
                featureLayer.popupLayerRemoved.connect(self.onPopupLayerRemoved)
                featureLayer.selectedFeatureChanged.connect(self.onSelectedFeatureChanged)
                featureLayer.currentTimeframeChanged.connect(lambda _: self.refreshUi())
        else:
            self._featureLayerId = None
        self.refreshUi()

    def getFeatures(self):
        """Get the Features."""
        if self.featureLayer:
            return [feature for feature in self.featureLayer.getFeatures()]
            # [feature for feature in self.featureLayer.getFeaturesInCurrentTimeframe()]
        else:
            return []
        

