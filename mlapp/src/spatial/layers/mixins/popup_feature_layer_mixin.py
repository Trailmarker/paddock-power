# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal

from ....widgets.feature_list.feature_layer_list import FeatureLayerList
from ...features.feature import Feature
from ..feature_layer import FeatureLayer
from .layer_mixin import LayerMixin

class PopupFeatureLayerMixin(LayerMixin):

    popupLayerAdded = pyqtSignal(Feature, FeatureLayer)
    popupLayerRemoved = pyqtSignal(Feature)

    def __init__(self):
        super().__init__()

        assert isinstance(self, FeatureLayer) or isinstance(self, FeatureLayerList)
