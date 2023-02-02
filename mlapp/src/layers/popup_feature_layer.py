# -*- coding: utf-8 -*-
from ..utils import randomString
from .derived_feature_layer import DerivedFeatureLayer


class PopupFeatureLayer(DerivedFeatureLayer):

    @classmethod
    def defaultName(cls):
        return f"{cls.__name__}{randomString()}"

    def __init__(self, feature, *args):
        DerivedFeatureLayer.__init__(self, *args)
        self.popupFeature = feature
