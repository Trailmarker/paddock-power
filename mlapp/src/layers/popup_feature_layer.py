# -*- coding: utf-8 -*-
from .derived_feature_layer import DerivedFeatureLayer


class PopupFeatureLayer(DerivedFeatureLayer):

    def __init__(self, feature, *args):
        DerivedFeatureLayer.__init__(self, *args)
        self.popupFeature = feature
